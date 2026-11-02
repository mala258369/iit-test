from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

soap_url = "https://activation.slmicrosoft.com/ProductActivationService.svc"
no_proxy = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""

    if request.method == "POST":
        iid = request.form.get("iid", "").strip()

        if not iid:
            result = "请输入安装IID"
        else:
            soap_body = f'''<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Action s:mustUnderstand="1">http://schemas.microsoft.com/2004/08/security/trust/Issue
                  </Action>
  </s:Header>
  <s:Body>
    <wst:Issue xmlns:wst="http://schemas.xmlsoap.org/ws/2004/09/security/trust">
      <wst:UseKey>
        <wst:TokenEntry>
          <wst:Claims>
            <wst:TokenEntry>
              <wst:Name>SessionKey</wst:Name>
              <wst:Value>{iid}</wst:Value>
            </wst:TokenEntry>
            <wst:TokenEntry>
              <wst:Name>产品密钥活动ID</wst:Name>
              <wst:Value>{iid}</wst:Value>
            </wst:TokenEntry>
          </wst:Claims>
        </wst:TokenEntry>
      </wst:UseKey>
    </wst:Issue>
  </s:Body>
</s:Envelope>'''

            headers = {
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://microsoft.com/SL/ProductActivationService/IssueToken"
            }

            try:
                resp = requests.post(
                    soap_url,
                    data=soap_body,
                    headers=headers,
                    timeout=20,
                    proxies=no_proxy,
                    verify=False
                )
                result = resp.text
            except Exception as e:
                result = f"请求失败：{str(e)}"

    return render_template_string(template_html, res=result)


template_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>获取确认ID</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        textarea {
            width: 100%;
            max-width: 640px;
            padding: 10px;
            font-size: 14px;
        }
        button {
            padding: 8px 20px;
            font-size: 14px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            white-space: pre-wrap;
            word-break: break-all;
            color: blue;
            border: 1px solid #ddd;
            padding: 10px;
            max-width: 640px;
            background: #f9f9f9;
        }
    </style>
</head>
<body>
    <h3>输入安装IID获取确认ID</h3>
    <form method="post">
        <textarea name="iid" rows="4" cols="60" placeholder="粘贴9组安装ID，空格隔开"></textarea>
        <br><br>
        <button type="submit">提交获取确认ID</button>
    </form>

    {% if res %}
    <div class="result">{{ res }}</div>
    {% endif %}
</body>
</html>'''


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=10000)
