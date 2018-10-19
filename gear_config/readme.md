

### 使用
```
在 config_utils.py 文件中 gear_user_list 加入你的名字，gear会搜索你的目录，来确定你是谁。
gear_save_root 为gear保留项，若使用自动训练戳功能，请保留此项。
修改config/下任意.yaml文件，在.yaml旁自动生成python类文件
from config.YOUR_CONFIG.XXXX.py import ARG
arg = ARG()

from config.YOUR_CONFIG.specificXXXX.py import ARG as sp_ARG
ap_arg = sp_ARG()

from config_utils import merge
arg = merge(arg, sp_arg)
```

### 修复
```
如果项目文件损坏,不能自动生成python类文件,请按readme_config.png图配置
```
