cd ../requirement
pip3 install -r requirements-aws.txt -t ./packages
cd packages
chmod -R 755 .
current_date_time="$(date +%F_%H-%M-%S)"
zip_name="workpay-payment-api-$current_date_time.zip"
zip -r9 ./../../publish/$zip_name *
cd ./../../publish
while [ ! -f $zip_name ];
do
  sleep 1 # or less like 0.2
done
cd ..
zip -ur ./publish/$zip_name * -x "env/*" -x "tests/*" -x "publish/*" -x "requirement/*"
sleep 1
aws s3 mv ./publish/$zip_name s3://workpay-test-lambda-resources --profile workpay