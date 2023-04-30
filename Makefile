.DEFAULT_GOAL := help

help:
	@echo 'venv: will create the python virtual env for the lambda development and deployment.'
	@echo 'show-skill-id: will show you your skillId if this is deployed.'
	@echo 'lambda-deploy: will deploy lambda function to AWS'
	@echo 'skill-deploy: will deploy your skill to yor Alexa developer console'
	@echo 'clean: will delete all temporal files and deployments files.'

show-skill-id:
	cat .ask/ask-states.json | grep "skillId"

venv:
	python3 -m venv venv/
	venv/bin/pip install -r lambda/requirements.txt

lambda-deploy: venv
	cd lambda && ../venv/bin/chalice deploy

skill-deploy:
	ask deploy

clean:
	pyclean .
	rm -rf .ask/
	rm -rf lambda/.chalice/deployed/
	rm -rf lambda/.chalice/deployments/
	rm -rf venv/
	
