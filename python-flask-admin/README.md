# admin portal

## Development guide
### Debug 
#### Run server  
```bash
# Create virtualenv with python3.7
virtualenv -p python3.7 env

# Activate virtualenv
source ./env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python run.py

```

### Production
##### Set FLASK_ENV=production in run-daemon.sh to tell flask run in production mode. 
```bash
# Go to provisioning folder and make next steps:
# Install node modules and build reactapp
./package.sh

# Build docker container
./build.sh

# Run container(change params in run-daemon.sh if needed)
./run-daemon.sh
```
