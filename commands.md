ps aux | grep '/opt/myapps/' | grep -v grep | awk '{print $2, $3, $4}' | while read pid cpu mem; do
    cmdline=$(ps -p $pid -o args=)
    echo "$pid $cpu $mem $cmdline"
done
