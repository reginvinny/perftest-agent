
## Performance Test Agent
A simple agent to execute shell scripts and serve results. Works well with popular CI/CD frameworks. The main reason to use perftest-agent would be to be avoid the network bottleneck that occurs with high throughput Jmeter tests using distributed mode. [[More info]](http://www.seleniumtests.com/2016/04/should-you-be-using-distributed-testing.html)

### Use case:

#### Run a load test and retrieve results via HTTP requests
Performance Test Agent can be used to trigger a load test if run on a load generator machine from CI/CD (egs: Jenkins).

- Make sure Jmeter is available in Load Generator machine
- Run Performance Test Agent
- Create a shell script to invoke the Jmeter test script
- Invoke the test script remotely via the agent ( PORT 7008) from Jenkins Plan
- Download test results via file server (PORT 7009) to Jenkins plan workspace


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





