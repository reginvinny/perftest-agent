
## Performance Test Agent
A simple agent to execute test scripts and serve results. Works well with popular CI/CD frameworks (Jenkins, Bamboo etc)

## Pre-requisites
- Python 2.7
- ZSH or BASH
- Linux / MacOS

## Performance Test Agent build steps
sh build/make.sh


## Performance Test Agent usage

```shell
export scriptHome=<script home path>
python perftest-agent.py &
```

>Default ports are 7008 and 7009 for agent and server respectively


## Performance Test Agent help

#### Invoke Test shell script : 
```shell
curl -d "script-path/script.sh http://[IP or DNS]:7008
```
#### Clear logs (Rotate) : 
```shell
curl -d "clear" http://[IP or DNS]:7008
```
#### Fetch test results : 
```shell
curl http://[IP or DNS]:7009
```
> Note: Target sh file must be present in the Script Home directory

#### Kill Performance Test Agent 
```shell
pkill -f perftest-agent.py

or 

fuser -k 7008/tcp #(Doesn't work on MacOS)

```

## IMPORTANT : READ BEFORE YOU USE THIS PROGRAM!

[LICENSE](./LICENSE)





