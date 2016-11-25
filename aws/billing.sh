aws --region us-east-1 cloudwatch get-metric-statistics \
    --namespace "AWS/Billing" \
    --metric-name "EstimatedCharges" \
    --dimension "Name=Currency,Value=USD" \
    --start-time $(date +"%Y-%m-%dT%H:%M:00" --date="-18 hours") \
    --end-time $(date +"%Y-%m-%dT%H:%M:00") \
    --statistic Maximum \
    --period 60 \
    --output text | sort -r -k 3 | head -n 1 | cut -f 2
