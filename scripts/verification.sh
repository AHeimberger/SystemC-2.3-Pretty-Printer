echo "Project Directory: ${DIR_PROJECT}"

pushd "${DIR_PROJECT}/verification/"
	python3 main.py
popd
