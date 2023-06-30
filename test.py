from dotenv import load_dotenv
import csv
import io
import os
import boto3

load_dotenv()

HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {os.environ.get("API_TOKEN")}',
    'X-GitHub-Api-Version': '2022-11-28'
}

ORGS = ['moloco', 'woowabros', 'daangn', 'toss', 'ncsoft', 'line', 'kakao', 'naver', 'nhn']

CSV_HEADER = [
    'id',
    'node_id',
    'name',
    'description',
    'company',
    'blog',
    'location',
    'email',
    'twitter_username',
    'followers',
    'following',
    'is_verified',
    'has_organization_projects',
    'has_repository_projects',
    'public_repos',
    'public_gists',
    'html_url',
    'avatar_url',
    'type',
    'created_at',
    'updated_at',
    'current_time',
]

s3 = boto3.client('s3',
    region_name='ap-northeast-2',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)

def api_to_csv() -> str:
    """
    API 정보를 읽어서 csv 형식의 문자열로 변환합니다.
    """
    output = io.StringIO()
    # API 대신 이미 읽어온 데이터 활용
    data = [(5779363, 'MDEyOk9yZ2FuaXphdGlvbjU3NzkzNjM=', 'MOLOCO', '', None, None, None, 'github@molocoads.com', None, 65, 0, False, True, True, 13, 0, 'https://github.com/moloco', 'https://avatars.githubusercontent.com/u/5779363?v=4', 'Organization', '2013-10-26T04:03:42Z', '2023-06-02T18:56:26Z', '2023-06-25'), (7642191, 'MDEyOk9yZ2FuaXphdGlvbjc2NDIxOTE=', 'woowabros', '', None, 'http://www.woowahan.com/', None, None, None, 72, 0, False, True, True, 20, 0, 'https://github.com/woowabros', 'https://avatars.githubusercontent.com/u/7642191?v=4', 'Organization', '2014-05-20T07:40:25Z', '2023-04-01T07:13:26Z', '2023-06-25'), (12152522, 'MDEyOk9yZ2FuaXphdGlvbjEyMTUyNTIy', '당근마켓', '당근마켓은 동네 이웃 간의 연결을 도와 따뜻하고 활발한 교류가 있는 지역 사회를 꿈꾸고 있어요.', None, 'https://www.daangn.com/', 'Korea, South', 'market@daangn.com', 'daangnteam', 475, 0, True, True, True, 107, 0, 'https://github.com/daangn', 'https://avatars.githubusercontent.com/u/12152522?v=4', 'Organization', '2015-04-28T11:36:56Z', '2022-08-23T14:54:32Z', '2023-06-25'), (25682207, 'MDEyOk9yZ2FuaXphdGlvbjI1NjgyMjA3', 'Toss', '', None, 'https://toss.im', 'Seoul, South Korea', None, None, 332, 0, True, True, True, 24, 0, 'https://github.com/toss', 'https://avatars.githubusercontent.com/u/25682207?v=4', 'Organization', '2017-02-10T08:09:52Z', '2023-03-17T05:51:40Z', '2023-06-25'), (15726364, 'MDEyOk9yZ2FuaXphdGlvbjE1NzI2MzY0', 'NCSOFT', 'NCSOFT Open Sources', None, 'http://www.ncsoft.com', 'Seoul, Korea', 'opensource@ncsoft.com', None, 71, 0, False, True, True, 32, 0, 'https://github.com/ncsoft', 'https://avatars.githubusercontent.com/u/15726364?v=4', 'Organization', '2015-11-09T08:48:20Z', '2021-12-24T08:05:16Z', '2023-06-25'), (13128444, 'MDEyOk9yZ2FuaXphdGlvbjEzMTI4NDQ0', 'LINE', '', None, 'https://engineering.linecorp.com/en/opensource', 'Tokyo, Japan', None, None, 568, 0, True, True, True, 107, 0, 'https://github.com/line', 'https://avatars.githubusercontent.com/u/13128444?v=4', 'Organization', '2015-07-01T03:07:36Z', '2023-05-15T01:51:12Z', '2023-06-25'), (1267113, 'MDEyOk9yZ2FuaXphdGlvbjEyNjcxMTM=', 'kakao', '', None, 'http://tech.kakao.com/', None, None, None, 278, 0, False, True, True, 54, 0, 'https://github.com/kakao', 'https://avatars.githubusercontent.com/u/1267113?v=4', 'Organization', '2011-12-16T05:06:15Z', '2023-02-02T08:14:53Z', '2023-06-25'), (6589568, 'MDEyOk9yZ2FuaXphdGlvbjY1ODk1Njg=', 'NAVER', '', None, 'http://developers.naver.com', 'Republic of Korea', 'opensource@navercorp.com', None, 886, 0, False, True, True, 230, 0, 'https://github.com/naver', 'https://avatars.githubusercontent.com/u/6589568?v=4', 'Organization', '2014-02-04T22:41:15Z', '2020-07-06T22:57:11Z', '2023-06-25'), (7907400, 'MDEyOk9yZ2FuaXphdGlvbjc5MDc0MDA=', 'NHN', '', None, None, 'Republic of Korea', 'oss@nhn.com', None, 414, 0, False, True, True, 104, 0, 'https://github.com/nhn', 'https://avatars.githubusercontent.com/u/7907400?v=4', 'Organization', '2014-06-16T23:25:30Z', '2022-02-15T08:01:42Z', '2023-06-25')]
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(CSV_HEADER) # 헤더 추가
    writer.writerows(data)
    print(output.getvalue())
    return output.getvalue()

def csv_to_s3(data: str):
    """
    CSV 데이터를 S3에 저장합니다.
    """
    s3.put_object(Bucket='ostracker', Key='test_collect/orgs/2023/06/27/collect.csv', Body=data)

def s3_to_csv():
    response = s3.get_object(Bucket='ostracker', Key='test_collect/orgs/2023/06/27/collect.csv')
    print(response)
    response['Body'].read().decode('utf-8')

print(api_to_csv())



# csv 형식 보고 가공 필요한지 확인. 
def csv_to_rds():
