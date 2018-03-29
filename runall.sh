TIMEFORMAT='%R seconds to build index'
time {
    ./index.sh varbyte ../dataset/*
}

TIMEFORMAT='%R seconds to wake server up'
time {
    ./make_dict.sh
}

TIMEFORMAT='%R seconds to search'
time {
    cat queries.txt | ./search.sh > queryres.txt
}

diff queryres.txt queryres_ok.txt
