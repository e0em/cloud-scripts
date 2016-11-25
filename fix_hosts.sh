HOSTS=`host  -t mx browan.com |cut -d" " -f 7|xargs -I{} host {}|cut -f 1,4  -d" "`
echo $HOST
