from flask import Flask, request, render_template_string
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

app = Flask(__name__)

soap_url = "https://activation.sls.microsoft.com/SLAActivateProduct/SLAActivateProduct.asmx?configextension=o14"
no_proxy = {"http": None, "https": None}
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

template_html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>IID转确认ID</title>
</head>
<body>
<h3>输入安装ID（IID）</h3>
<form method="post">
<textarea name="iid" rows="4" cols="60" placeholder="粘贴9组安装ID，空格隔开"></textarea>
<br>
<button type="submit">提交获取确认ID</button>
</form>
{% if res %}
<div style="margin-top:20px">
结果：{{res}}
</div>
{% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET','POST'])
def index():
    result = ""
    if request.method == "POST":
        iid = request.form.get("iid","").strip()
        soap_body = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
            '<s:Header>'
            '<Action s:mustUnderstand="1">http://schemas.xmlsoap.org/ws/2004/09/security/trust/Issue</Action>'
            '</s:Header>'
            '<s:Body>'
            '<wst:Issue xmlns:wst="http://schemas.xmlsoap.org/ws/2004/09/security/trust">'
            '<wst:UseKey>'
            '<wst:TokenEntry>'
            '<wst:Name>发布许可证</wst:Name>'
            f'<wst:Value>{iid}</wst:Value>'
            '</wst:TokenEntry>'
            '</wst:UseKey>'
            '<wst:Claims>'
            '<wst:TokenEntry>'
            '<wst:Name>SessionKey</wst:Name>'
            '<wst:Value></wst:Value>'
            '</wst:TokenEntry>'
            '<wst:TokenEntry>'
            '<wst:Name>产品密钥活动ID</wst:Name>'
            '<wst:Value></wst:Value>'
            '</wst:TokenEntry>'
            '</wst:Claims>'
            '</wst:Issue>'
            '</s:Body>'
            '</s:Envelope>'
        )
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "http://microsoft.com/SL/ProductActivationService/IssueToken"
        }
        try:
            resp = requests.post(soap_url, data=soap_body, headers=headers, timeout=20, proxies=no_proxy, verify=False)
            result = resp.text
        except Exception as e:
            result = f"请求失败：{str(e)}"
    return render_template_string(template_html, res=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0")