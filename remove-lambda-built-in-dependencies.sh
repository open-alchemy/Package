cat requirements.txt \
    | sed '/boto/d' \
    | sed '/jmespath/d' \
    | sed '/python-dateutil/d' \
    | sed '/s3transfer/d' \
    | sed '/urllib3/d' \
    | sed '/six/d' \
    | tee lambda-requirements.txt
