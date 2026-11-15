import boto3, json, mimetypes, os
from botocore.client import Config
from pathlib import Path

# Credentials — set via environment variables or .env file (never hardcode)
# export COS_ACCESS_KEY_ID=<your_hmac_access_key>
# export COS_SECRET_ACCESS_KEY=<your_hmac_secret_key>
ACCESS_KEY = os.environ.get('COS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('COS_SECRET_ACCESS_KEY')
ENDPOINT   = os.environ.get('COS_ENDPOINT', 'https://s3.eu-gb.cloud-object-storage.appdomain.cloud')
BUCKET     = os.environ.get('COS_BUCKET', 'clara-website-37732a34')

if not ACCESS_KEY or not SECRET_KEY:
    raise EnvironmentError(
        "Missing credentials. Set COS_ACCESS_KEY_ID and COS_SECRET_ACCESS_KEY "
        "as environment variables before running this script.\n"
        "Example:\n"
        "  $env:COS_ACCESS_KEY_ID='<key>'\n"
        "  $env:COS_SECRET_ACCESS_KEY='<secret>'\n"
        "  python scripts/deploy_cos.py"
    )

cos = boto3.client('s3', endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version='s3v4'), region_name='eu-gb')

# --- Step 1: find valid LocationConstraint ---
valid_loc = None
for loc in ['eu-gb', 'eu-gb-standard', 'eu-gb-smart', 'eu-gb-flex',
            'eu-standard', 'us-south', 'us-south-standard']:
    test_bucket = 'clara-loc-test-' + loc.replace('-', '')[:6]
    try:
        cos.create_bucket(Bucket=test_bucket,
            CreateBucketConfiguration={'LocationConstraint': loc})
        cos.delete_bucket(Bucket=test_bucket)
        valid_loc = loc
        print('Valid LocationConstraint:', loc)
        break
    except Exception as e:
        msg = str(e)
        if 'InvalidLocationConstraint' in msg or 'not available' in msg.lower():
            print('  skip', loc)
        elif 'BucketAlreadyOwned' in msg or 'exists' in msg.lower():
            valid_loc = loc
            print('Already owned with loc:', loc)
            break
        else:
            print('  err', loc, msg[:80])

if not valid_loc:
    # Try without LocationConstraint
    try:
        cos.create_bucket(Bucket='clara-loc-test-plain')
        cos.delete_bucket(Bucket='clara-loc-test-plain')
        valid_loc = None
        print('Works without LocationConstraint')
    except Exception as e:
        print('No valid location found:', e)
        exit(1)

# --- Step 2: Create the website bucket ---
try:
    if valid_loc:
        cos.create_bucket(Bucket=BUCKET,
            CreateBucketConfiguration={'LocationConstraint': valid_loc})
    else:
        cos.create_bucket(Bucket=BUCKET)
    print('Bucket created:', BUCKET)
except Exception as e:
    if 'BucketAlreadyOwned' in str(e) or 'owned' in str(e).lower():
        print('Bucket already exists, continuing...')
    else:
        print('Create bucket error:', e); exit(1)

# --- Step 3: Static website hosting ---
cos.put_bucket_website(Bucket=BUCKET,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'index.html'},
        'ErrorDocument': {'Key': 'index.html'}
    })
print('Static hosting enabled')

# --- Step 4: Public ACL on bucket ---
cos.put_bucket_acl(Bucket=BUCKET, ACL='public-read')
print('Public read ACL applied')

# --- Step 5: Upload website files with public-read ACL ---
website_dir = Path('website')
for f in sorted(website_dir.iterdir()):
    if f.is_file():
        mime, _ = mimetypes.guess_type(str(f))
        mime = mime or 'application/octet-stream'
        cos.upload_file(str(f), BUCKET, f.name,
            ExtraArgs={'ContentType': mime, 'CacheControl': 'max-age=300',
                       'ACL': 'public-read'})
        print('  Uploaded:', f.name, '(' + mime + ')')

print()
print('=== SITE URL ===')
print('https://' + BUCKET + '.s3-web.eu-gb.cloud-object-storage.appdomain.cloud')
