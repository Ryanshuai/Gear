

### 使用
```
1, 在 config_utils.py 文件中 gear_user_list 加入你的名字，gear会搜索你的目录，来确定你是谁。
2, 修改config/下任意.yaml文件，gear会在.yaml旁自动生成python类文件。
3, 在你的程序中引用ARG类。
    from config.YOUR_CONFIG.XXXX.py import ARG
    arg = ARG()
    
    from config.YOUR_CONFIG.specificXXXX.py import ARG as sp_ARG
    ap_arg = sp_ARG()
    
    from config_utils import merge
    arg = merge(arg, sp_arg)
    
(gear_save_root 为gear保留项，若使用自动训练戳功能，请保留此项。自动训练戳包含用户名、配置名和运行时间。)
(自动生成功能是配置pycharm插件filewatcher得到的。若在非pycharm环境下，请手动 python generate_py_class_file.py)
```
### 修复
```
如果项目文件损坏,不能自动生成python类文件,请按readme_config.png图配置
```
