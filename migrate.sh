alembic stamp head 
alembic revision --autogenerate -m "$1"
echo "Do you want to migrate? [y/n]"
read input
if [ "$input" == "y" ]
then
  alembic upgrade head
else
  echo "Aborting..."
fi