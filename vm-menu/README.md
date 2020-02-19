A little bash abomination I wrote to control my windows VM. Everything is hard-coded because I'm lazy.

Functionality:
right click on shut off VM to turn it on
right click on running VM to show menu
left click on menu items to run respective scripts and close the menu

all files from bin folder should be somewhere in PATH

polybar config:

[module/checkVM]
type = custom/script
tail = true
label = %output%
exec = path/to/vm-main.sh

format-prefix-foreground = ${colors.foreground-alt}
format-prefix = VM:
format-prefix-underline = ${colors.background}
format-underline = ${colors.primary}
