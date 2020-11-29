#!/bin/bash

# Global settings
BOOL_DO_SHUFFLE=1  # If true then we shuffle files
RESEARCHES_NB_FILES=10000  # Just before starting the research requests, we generate an IF based on that number of files to parse.
PYTHON_EXEC=python

# Initial config
SCRIPT_BUILD_PYFILE="$PYTHON_EXEC ../src/main_build_and_save_if.py"
if [[ $BOOL_DO_SHUFFLE -eq 1 ]]
then
    BUILD_SCRIPT_SHUFFLE_ARG="--shufflefiles"
else
    BUILD_SCRIPT_SHUFFLE_ARG=""
fi
NB_FILES_RANGE="1 2 5 5 10 20 50 100"
SCRIPT_REQUEST_PYFILE="$PYTHON_EXEC ../src/main_requests.py"

function Fct_Run_Loop {
    Do_Save=$1
    Voc_Type=$2

    if [[ $Do_Save -eq 1 ]]
    then
        Script_Save_Arg=""
    else
        Script_Save_Arg="--do_not_save"
    fi
    rm -f *.bin
    echo "Script_Save_Arg=$Script_Save_Arg Voc_Type=$Voc_Type"

    echo "Run with VOC = $Voc_Type and PL_MMap usage is $Do_Save"
    for nb_files in $NB_FILES_RANGE
    do
        run_cmd="$SCRIPT_BUILD_PYFILE --nbfiles $nb_files $BUILD_SCRIPT_SHUFFLE_ARG $Script_Save_Arg --time --memory --voc_type $Voc_Type"

        run_stdout=$($run_cmd)
        run_exitcode=$?
        if [[ $run_exitcode -ne 0 ]]
        then
            echo "Error, run failed with exit code $run_exitcode"
            exit 1
        fi
        run_runtime=$(echo $run_stdout | awk '{print $2;}')
        run_memory=$(echo  $run_stdout | awk '{print $4;}')

        echo "Nb_Files= $nb_files runtime= $run_runtime ms run_memory= $run_memory bytes"
        rm -f *.bin
    done

    echo ""
}

function Fct_Run_Request {
    Keywords=$1
    Voc_Type=$2
    CSV_File=$3

    echo "Run with VOC = $Voc_Type and with the following keywords : $Keywords "
    for nb_files in $NB_FILES_RANGE
    do
        # Create all the bin files
        if [[ $Do_Save -eq 1 ]]
        then
            Script_Save_Arg=""
        else
            Script_Save_Arg="--do_not_save"
        fi
        rm -f *.bin

        run_cmd="$SCRIPT_BUILD_PYFILE --nbfiles $nb_files $BUILD_SCRIPT_SHUFFLE_ARG --time --memory --voc_type $Voc_Type"
        run_stdout=$($run_cmd)
        run_exitcode=$?
        if [[ $run_exitcode -ne 0 ]]
        then
            echo "Error, run failed with exit code $run_exitcode"
            exit 1
        fi

        # Run the requests
        run_cmd="$SCRIPT_REQUEST_PYFILE --request \"$nb_files\"  --time --memory --voc_type $Voc_Type"

        run_stdout=$($run_cmd | tail -1)
        run_exitcode=$?
        if [[ $run_exitcode -ne 0 ]]
        then
            echo "Error, run failed with exit code $run_exitcode"
            exit 1
        fi

        run_runtime=$(echo $run_stdout | awk '{print $2;}')
        run_memory=$(echo  $run_stdout | awk '{print $4;}')

        echo "$Keywords,$nb_files,$run_runtime,$run_memory" >> "$CSV_File"
        echo "Nb_Files= $nb_files runtime= $run_runtime ms run_memory= $run_memory bytes"
        rm -f *.bin
    done

    echo ""
}

# Run scripts in which we generate the IFs.
# Fct_Run_Loop 0 "VOC_Hashmap"
# Fct_Run_Loop 0 "VOC_BTree"
# Fct_Run_Loop 1 "VOC_Hashmap"

# Run scripts to automate queries VOC_HashMap
#Fct_Run_Request "said" "VOC_Hashmap" "popular_hashmap.csv"
#Fct_Run_Request "zayak" "VOC_Hashmap" "rare_hashmap.csv"

Fct_Run_Request "said" "VOC_BTree" "test.csv"


# Prepare research commands
#$SCRIPT_BUILD_PYFILE --nbfiles $RESEARCHES_NB_FILES $BUILD_SCRIPT_SHUFFLE_ARG --voc_type "VOC_Hashmap"

#CSV >> colonnes moyenne temps d'éxécution de chaque type de requêtes
