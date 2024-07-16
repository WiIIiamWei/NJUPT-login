# NJUPT-login

南京邮电大学校园网登录脚本。大概是Python新手的第一次尝试（不要喷我）。

[English](https://github.com/WiIIiamWei/NJUPT-login/blob/main/README-EN.md)

## 如何使用

**! 请注意：本脚本会在当前文件夹生成config.bin储存你的登录信息，请不要随意删除或传播该文件，此举会导致你的密码泄露！**

您可以直接在Release界面找到使用`pyinstaller`生成的可执行文件，也可以下载源代码直接运行（需要`requests`库）。

推荐您将可执行文件单独放在一个文件夹里，然后创建桌面快捷方式或将快捷方式放到“启动”文件夹内开机自启（也可创建计划任务）。

## 其他的方案

### 使用`curl`进行登录请求

对于校园网账户，可以使用以下命令：

```bash
curl --insecure "https://p.njupt.edu.cn:802/eportal/portal/login?&&user_account=<BID>&&user_password=<PASSWORD>"
```

对于中国移动账户，可以使用以下命令：

```bash
curl --insecure "https://p.njupt.edu.cn:802/eportal/portal/login?&&user_account=<BID>%40cmcc&&user_password=<PASSWORD>"
```

对于中国电信账户，可以使用以下命令：

```bash
curl --insecure "https://p.njupt.edu.cn:802/eportal/portal/login?&&user_account=<BID>%40njxy&&user_password=<PASSWORD>"
```

使用时，请将`<BID>`替换为自己的学号，`<PASSWORD>`替换为自己的统一身份验证密码。

**此方法不适用于Windows PowerShell中的`curl`，因为其已被alias为`Invoke-WebRequest`。若想在Windows上设置，您可使用Cygwin或Git Bash等其他shell，或者安装适用于Windows的`curl`，或参照下方方案使用`Invoke-WebRequest`。**

您还可以为此命令设置alias，以便能在您的shell中使用。例如，对于bash和zsh，请分别在`.bashrc`和`.zshrc`（通常位于`~/.bashrc`或`~/.zshrc`）加入以下行：

```bash
alias njupt-login='curl --insecure "https://p.njupt.edu.cn:802/eportal/portal/login?&&user_account=<BID>&&user_password=<PASSWORD>"'
```

*请根据您的账户类型选择正确的URL（参照`curl`中的URL），以上仅为一个例子。*

### 使用`Invoke-WebRequest`进行登录请求

使用以下命令：

```powershell
Invoke-WebRequest -Uri "https://p.njupt.edu.cn:802/eportal/portal/login?&&user_account=<BID>&&user_password=<PASSWORD>" -UseBasicParsing
```

*请根据您的账户类型选择正确的URL（参照`curl`中的URL），以上仅为一个例子。*

若需要在PowerShell中创建alias，您可以在`$profile$`加入下列函数（可以通过在PowerShell中键入`$profile$`找到该文件的位置）：

```powershell
function njupt-login {
    $response = Invoke-WebRequest -Uri "https://p.njupt.edu.cn:802/eportal/portal/login?&&user_account=<BID>&&user_password=<PASSWORD>" -UseBasicParsing
    $response.Content
}
```

*请根据您的账户类型选择正确的URL（参照`curl`中的URL），以上仅为一个例子。*

## 版权声明

本项目的可执行程序图标使用了南京邮电大学商标（仅为方便辨识使用，如涉及侵权请与我联系），此商标版权归南京邮电大学所有。

其余所有的项目代码均遵守GNU GPLv3协议。
