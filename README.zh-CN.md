# Repo README Polisher

<p align="center">
  <strong>鎶婁竴涓櫘閫氶」鐩洰褰曪紝鏁寸悊鎴愭洿鍍忔牱鐨?GitHub README 鑽夌銆?/strong>
</p>

<p align="center">
  <a href="README.md">English</a> 路
  <a href="#蹇€熷紑濮?>蹇€熷紑濮?/a> 路
  <a href="#璺嚎鍥?>璺嚎鍥?/a> 路
  <a href="CONTRIBUTING.md">璐＄尞鎸囧崡</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg">
  <img alt="Status" src="https://img.shields.io/badge/Status-Alpha-orange">
  <img alt="Runtime" src="https://img.shields.io/badge/Runtime-stdlib--only-blue">
</p>

---

`repo-readme-polisher` 鏄竴涓交閲忕骇鍛戒护琛屽伐鍏凤紝鍙互鎵弿鏈湴椤圭洰鐩綍锛屽苟鐢熸垚缁撴瀯娓呮櫚銆侀€傚悎 GitHub 灞曠ず鐨?`README_DRAFT.md`銆?
瀹冮€傚悎閭ｄ簺鈥滀唬鐮佸凡缁忓啓浜嗭紝浣嗛」鐩粙缁嶈繕鍍忓崐鎴愬搧鈥濈殑浠撳簱锛氳嚜鍔ㄦ暣鐞嗗姛鑳姐€佹妧鏈爤銆佸揩閫熷紑濮嬨€侀」鐩粨鏋勩€佽矾绾垮浘鍜屼綔鍝侀泦浜偣銆?
鏃犻渶 API Key锛屼笉渚濊禆浜戞湇鍔★紝涓嶄笂浼犱綘鐨勪唬鐮併€傜涓€鐗堝畬鍏ㄦ湰鍦拌繍琛岋紝鍩轰簬瑙勫垯鎵弿椤圭洰缁撴瀯骞剁敓鎴?README 鑽夌銆?
## 椤圭洰浜偣

- **鏈湴浼樺厛**锛氬彧鎵弿鏈湴鐩綍锛屼笉鎶婃枃浠跺彂閫佸埌澶栭儴鏈嶅姟銆?- **闆惰繍琛屾椂渚濊禆**锛氬熀浜?Python 鏍囧噯搴撳疄鐜般€?- **鎶€鏈爤鎰熺煡**锛氳瘑鍒?Python銆丣avaScript/TypeScript銆乂ue銆丷eact銆丣ava銆丼pring Boot銆丏ocker 绛夊父瑙侀」鐩壒寰併€?- **GitHub 鍙嬪ソ杈撳嚭**锛氳嚜鍔ㄧ敓鎴愬姛鑳姐€佹妧鏈爤銆佸揩閫熷紑濮嬨€佹祴璇曘€佽矾绾垮浘銆佽鍙瘉绛夌珷鑺傘€?- **閫傚悎浣滃搧闆?*锛氬府鍔╂妸鏅€氱粌鎵嬮」鐩暣鐞嗘垚鏇村鏄撳睍绀哄拰璁叉竻妤氱殑浠撳簱銆?
## 蹇€熷紑濮?
```bash
git clone https://github.com/Zeweir/repo-readme-polisher.git
cd repo-readme-polisher

python -m pip install -e .
repo-readme-polisher path/to/your-project
```

涔熷彲浠ョ洿鎺ョ敤妯″潡鏂瑰紡杩愯锛?
```bash
python -m repo_readme_polisher path/to/your-project
```

榛樿浼氱敓鎴愶細

```text
README_DRAFT.md
```

## 浣跨敤鏂瑰紡

涓哄綋鍓嶇洰褰曠敓鎴愯崏绋匡細

```bash
repo-readme-polisher .
```

涓哄叾浠栭」鐩敓鎴愯崏绋匡細

```bash
repo-readme-polisher ../my-project
```

鎸囧畾杈撳嚭璺緞锛?
```bash
repo-readme-polisher ../my-project -o docs/README_DRAFT.md
```

杈撳嚭鍒扮粓绔細

```bash
repo-readme-polisher ../my-project --stdout
```

鎸囧畾椤圭洰鏍囬锛?
```bash
repo-readme-polisher ../my-project --title "My Awesome Project"
```

## 鑳借瘑鍒粈涔?
| 绫诲瀷 | 绀轰緥 |
| --- | --- |
| 璇█ | Python銆丣avaScript/TypeScript銆丣ava銆乂ue銆丟o |
| 鍖呯鐞?鏋勫缓鏂囦欢 | `pyproject.toml`銆乣requirements.txt`銆乣package.json`銆乣pom.xml`銆乣build.gradle` |
| 鍓嶇宸ュ叿 | React銆乂ue銆乂ite銆丯ext.js銆乀ailwind CSS |
| 鍚庣宸ュ叿 | Express銆丗astify銆丼pring Boot |
| 閮ㄧ讲绾跨储 | `Dockerfile`銆乣docker-compose.yml`銆乣.env.example` |
| 椤圭洰瑙勮寖 | `LICENSE`銆乣tests/`銆佸凡鏈?`README.md` |

## 绀轰緥杈撳嚭

鏌ョ湅 [`examples/README_DRAFT.sample.md`](examples/README_DRAFT.sample.md)銆?
## 鏋舵瀯

```mermaid
flowchart TD
    A[椤圭洰鐩綍] --> B[鎵弿鍣╙
    B --> C[鍏抽敭鏂囦欢璇嗗埆]
    B --> D[鐩綍缁撴瀯鎽樿]
    C --> E[鎶€鏈爤妫€娴媇
    D --> F[README 鐢熸垚鍣╙
    E --> F
    F --> G[README_DRAFT.md]
```

## 椤圭洰缁撴瀯

```text
.
鈹溾攢鈹€ .github/
鈹?  鈹溾攢鈹€ ISSUE_TEMPLATE/
鈹?  鈹斺攢鈹€ workflows/
鈹溾攢鈹€ docs/
鈹溾攢鈹€ examples/
鈹溾攢鈹€ repo_readme_polisher/
鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ __main__.py
鈹?  鈹溾攢鈹€ detector.py
鈹?  鈹溾攢鈹€ generator.py
鈹?  鈹斺攢鈹€ scanner.py
鈹溾攢鈹€ tests/
鈹溾攢鈹€ CHANGELOG.md
鈹溾攢鈹€ CODE_OF_CONDUCT.md
鈹溾攢鈹€ CONTRIBUTING.md
鈹溾攢鈹€ LICENSE
鈹溾攢鈹€ README.md
鈹溾攢鈹€ README.zh-CN.md
鈹溾攢鈹€ SECURITY.md
鈹斺攢鈹€ pyproject.toml
```

## 寮€鍙?
杩愯娴嬭瘯锛?
```bash
python -m pytest
```

浠庡綋鍓嶄粨搴撶敓鎴愮ず渚嬭崏绋匡細

```bash
python -m repo_readme_polisher . -o examples/README_DRAFT.sample.md
```

## 璺嚎鍥?
- [x] 鏈湴椤圭洰鎵弿鍣?- [x] 瑙勫垯寮忔妧鏈爤妫€娴?- [x] README 鑽夌鐢熸垚鍣?- [x] 绀轰緥杈撳嚭
- [x] GitHub Actions CI
- [ ] 鏇翠赴瀵岀殑妗嗘灦璇嗗埆
- [ ] Markdown 璐ㄩ噺璇勫垎
- [ ] 鍙厤缃?README 妯℃澘
- [ ] 鍙€?AI 鏀瑰啓妯″紡锛歚--ai`
- [ ] GitHub 浠撳簱鍏冩暟鎹敮鎸?- [ ] 寰界珷鍜屾埅鍥惧缓璁?
## 璐＄尞

娆㈣繋璐＄尞銆傝鏌ョ湅 [CONTRIBUTING.md](CONTRIBUTING.md)銆?
濡傛灉浣犳兂鏂板妫€娴嬪櫒锛岃灏介噺鎻愪緵锛?
1. 瑕佹娴嬬殑鏂囦欢鎴栦緷璧栧悕绉帮紱
2. 涓€涓渶灏忛」鐩粨鏋勭ず渚嬶紱
3. 鏈熸湜鐢熸垚鐨?README 鍐呭銆?
## 瀹夊叏

鏈伐鍏峰彧搴旇鍙栨湰鍦伴」鐩厓鏁版嵁锛屼笉搴斾笂浼犱綘鐨勬枃浠舵垨瀵嗛挜銆?
濡傛灉浣犲彂鐜板畨鍏ㄩ棶棰橈紝璇锋煡鐪?[SECURITY.md](SECURITY.md)銆?
## 璁稿彲璇?
鏈」鐩熀浜?MIT License 寮€婧愩€傝瑙?[LICENSE](LICENSE)銆?
