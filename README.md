# Fuzzyman
Fuzzyman takes your Openapi 2.0 spec and creates a fuzzed collection of your API to help discover bugs and vulnerabilities. The tests can be run with postman runners.
## Up and Running
Fuzzyman can be hosted, but its intended use is to run on a local machine with docker-compose.

Steps to run locally:

1) Clone the project from [here](https://github.com/ekivolowitz/FuzzyMan)
2) In the root level of `FuzzyMan`, create a `.env` file with the following contents:
```.env
POSTMAN_API_KEY=<Your Postman API key goes here>
```
3) Run `docker-compose build` from the root directory of `Fuzzyman`.
4) Run `docker-compose up`
5) Visit `https://localhost` in your web browser, or see this https://www.postman.com/galactic-shuttle-665520/workspace/postman-hackathon
for an example of using Fuzzyman as an api.