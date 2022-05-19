import os
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.getenv("APP_ENV", default="DEV")

if ENV == "PRD":
    WSDL = "lib/wsdl/credifamilia-prd.wsdl"
else:
    WSDL = "https://demo-servicesesb.datacredito.com.co/wss/dhws3/services/DHServicePlus?WSDL"


EXPIRES_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

sentry_sdk.init(
    dsn="https://82569d4f1ab94d708d8d51bb89b99618@o412045.ingest.sentry.io/5288222",
    integrations=[AwsLambdaIntegration()],
    traces_sample_rate=1.0,  # adjust the sample rate in production as needed
    environment=ENV,
)

USERNAME = "2-900986913"  # TODO: os.getenv('USERNAME')
PASSWORD = "gq4Yum7e4Fry"

CERTIFICATE_PATH = os.path.join(BASE_DIR, "lib", "certs", "certificate.pem")
KEY_PATH = os.path.join(BASE_DIR, "lib", "certs", "key.pem")
