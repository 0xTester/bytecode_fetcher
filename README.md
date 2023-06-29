# bytecode_fetcher
A small script to get the bytecode of any deployed smart contract.

_______________________________________________________________________________________________________________________________________________________________________________________________
NOTE: Remember to change the auth credentials with your own.
      I recommend to work in a virtual environment and set the credentials in the ./activate file, this way I don't have "oh shit i forgot to add the .env file to gitignore" problems, however
      you can use any option (.env file environment variables or ./activate file environment variables)
_______________________________________________________________________________________________________________________________________________________________________________________________

- This script returns the bytecode of any **SUCCESSFULY DEPLOYED** contract (failed deployments are ignored). 
- This script returns the **RUNTIME bytecode** of the contracts.
