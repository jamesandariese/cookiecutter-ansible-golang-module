### Testing

To test this module with the included docker test suite, you must build the
docker image from the project root (next to `cookiecutter.json`) and run it.

```bash
[ -f cookiecutter.json ] || echo "WRONG DIRECTORY EXPECT ERRORS"
docker build -t test-cookiecutter-ansible-$$ . -f test/Dockerfile
docker run test-cookiecutter-ansible-$$
if [ $? -eq 0 ];then
    echo success
else
    echo failure
    false  # preserve the exit status
fi
```
