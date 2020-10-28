from django.http import HttpResponse
from AWSProj.settings import s3_client
from django.shortcuts import render,redirect
from django.contrib import messages


def list_buckets():
    response = s3_client.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])
    return buckets


def file_upload(request):
    if request.method == 'POST':
        image_file = request.FILES['upload_file']
        bucket_name = "kelidari"
        name_in_bucket = image_file.name.replace(" ", "_")
        try:
            s3_client.upload_fileobj(Fileobj=image_file, Bucket=bucket_name, Key=name_in_bucket)
            s3_client.put_object_acl(ACL='public-read',Key=name_in_bucket, Bucket=bucket_name)
        except:
            messages.error(request,'آپلود فایل با مشکل مواجه شد! دوباره سعی کنید')
    messages.success(request, "فایل با موفقیت بارگزاری شد")
    return redirect('aws:download')


def get_bucket_keys(bucket):
    """Get a list of keys in an S3 bucket."""
    keys = []
    try:
       resp = s3_client.list_objects_v2(Bucket=bucket)
       for obj in resp['Contents']:
           keys.append(obj['Key'])
       return keys
    except :
        return HttpResponse('bucket '+bucket+' is empty ! pleas upload one')


def file_download(request):
    bucket_name = "kelidari"
    key=get_bucket_keys(bucket_name)
    return render(request, 'download.html', {'key': key})


def file_delete(request):

    bucket_name = "kelidari"
    key = request.GET['key']

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)


    except:

        messages.error(request, 'حذف فایل با مشکل مواجه شد! دوباره سعی کنید')
    messages.success(request, "فایل با موفقیت حذف شد")
    return redirect('aws:download')

