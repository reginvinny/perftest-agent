
## Performance Test Agent
A simple agent to execute test scripts and serve results. Works well with popular CI/CD frameworks (Jenkins, Bamboo etc)

## Pre-requisites
- Python 2.7
- ZSH or BASH

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

## Legal Disclaimer

> This software is made available with NO representations or warranties of any kind about the completeness, accuracy, reliability, suitability or availability for any purpose. Any reliance you place on this software is therefore strictly at your own risk.

> In no event will the developer be liable for any loss or damage including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits arising out of, or in connection with, the use of this software.




