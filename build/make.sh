#Output file will be created in "out" folder

SCRIPTPATH=$(dirname "$0")
OUT_PATH=out/perftest-agent.zip

cd $SCRIPTPATH
rm -rf out/*
mkdir -p out
zip -r "$OUT_PATH" ../perftest-agent.py

echo "Output file generated : $SCRIPTPATH/$OUT_PATH"