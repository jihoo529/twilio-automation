import re

text = '''貴為{{你好}}特選客戶，現選用📺 Now TV有【驚喜至抵優惠】🤫

【{{你好2}}】

特選客戶🔥限時優惠🔥至激賞🎁✨

即刻撳以下👇🏻按鈕去解鎖驚喜㊙️

優惠期有限，受條款及細則約束。'''

pattern = r"\{\{([^}]+)\}\}"
matches = re.findall(pattern, text)
num_variables = len(matches)
print(num_variables)
replaced_text = re.sub(pattern, lambda m: f"{{{{{matches.index(m.group(1))+1}}}}}", text)

variables = {i+1: match for i, match in enumerate(matches)}

print(variables)

url = "https://here2serve--uatc.sandbox.file.force.com/sfc/dist/version/renditionDownload?rendition=ORIGINAL_Png&versionId=068BU0000009yPx&operationContext=DELIVERY&contentId=05TBU000000OMc5&page=0&d=/a/BU0000000jrZ/fQSbyRBmaxuHanxWRsO782wMXn0rJ.U7kFnLluhUKuk&oid=00D9D0000008f4n&dpt=null&viewId="
pattern2 = r"(?<=version/)(.*)"

replaced_url = re.sub(pattern2, "{{1}}", url)
match = re.search(pattern2, url)
print(replaced_url)
print(match.group(1))