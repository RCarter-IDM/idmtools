#!/usr/bin/env bash

VIRTUALENV_DIR="$(mktemp -d)"
echo "env" $VIRTUALENV_DIR
trap 'rm -r "${VIRTUALENV_DIR}"' EXIT
virtualenv -p python3.6 "${VIRTUALENV_DIR}"
source "${VIRTUALENV_DIR}/bin/activate"

echo "install idmtools ..."
LOCAL_PATH="$(realpath $(dirname '$0')/)"
echo ${LOCAL_PATH}
cd ${LOCAL_PATH}/idmtools_core && \
    pip install -e .\[test,3.6\] --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple
cd ${LOCAL_PATH}/idmtools_local_runner && \
    pip install -e .\[test\]
cd ${LOCAL_PATH}/idmtools_models_collection && \
    pip install -e .\[test\]
# ensure we don't have a copy running and previous instances have been stopped
cd ${LOCAL_PATH}/idmtools_local_runner && \
	docker-compose down -v && \
	docker-compose build && \
	./start.sh

echo "auto login..."
cd ${LOCAL_PATH}/idmtools_core/tests && \
   python create_auth_token_args.py --comps_url "$1" --username "$2" --password "$3"
   #python create_auth_token_args.py --comps_url "https://comps2.idmod.org" --username "shchen" --password "Password123"

echo "run all tests..."
cd ${LOCAL_PATH}/idmtools_core/tests
python run_tests.py

echo "deactivate..."
deactivate
