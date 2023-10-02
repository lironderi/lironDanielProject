# *DevOps Project*

This DevOps portfolio project demonstrates the software development lifecycle end-to-end by  implementing DevOps methodologies.
It highlights the importance of DevOps practices in streamlining the process from ideation to continuous delivery.


## *Project Repos*
- [Web-App](https://github.com/lironderi/project_app)
- [infrastructure](https://github.com/lironderi/project_conf)

## *Project Details*
The project employs various technologies and methodologies:
- *Front-end*: CSS, HTML are used for developing the website's front-end.
- *Back-end*: Flask is used to create a REST API to connect with the website's front-end.
- *Database*: MongoDB is used to store and manage data in the application.

 CI/CD: Implements CI through automated testing in GitHub Actions, while triggering infrastructure repo that enables CD by using ArgoCD
- *Test*: Pytest provides automated unit testing that validates code correctness and detects regressions before they impact users.
- *Containerize*: Docker packages the validated application into a portable image, uploads it to DockerHub registry for distribution.
- *Trigger*: By updating the Docker image version in the infrastructure repository and pushing changes, an automated ArgoCD deployment is triggered.
- *Notify*: When a failure occurs in the workflow, email notifications are responsively sent to quickly make the developer aware
