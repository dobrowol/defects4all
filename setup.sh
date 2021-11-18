if [[ -z "${DEFECTS4ALL_ENV}" ]]; then
    DEFECTS4ALL_ENV=`pwd`
fi
if [[ -z "${PARSED_LOGS_ENV}" ]]; then
    PARSED_LOGS_ENV="$DEFECTS4ALL_ENV/parsed_logs"
fi
if [[ -z "${FASTTEXT_ENV}" ]]; then
    if [[ ! -d fastText-0.9.2 ]]; then
	    `wget https://github.com/facebookresearch/fastText/archive/v0.9.2.zip`
	    unzip v0.9.2.zip
	    cd fastText-0.9.2
	    make
    else
	    cd fastText-0.9.2
    fi 
    echo `pwd`
    export FASTTEXT_ENV=`pwd`
    echo "FASTTEXT_ENV $FASTTEXT_ENV"
    cd ..
fi
shopt -s nocasematch
if ! [[ "${PYTHONPATH}" =~ "drain3"  ]]; then
	echo "Drain3 not in PYTHONPATH!!!"
fi
