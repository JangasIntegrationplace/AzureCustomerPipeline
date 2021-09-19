## Terraform
This project includes Infrastructure as Code (IaC) by using
Terraform. Since the focus of this project should be a poc
the setup is not hyper secure. No Role Based Access (RBA)
for resources or key vault is included.

### Local
1. If not already happen, install Terraform at your system. You can 
    follow these steps: https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/azure-get-started
2. If not already happen, install Azure CLI
3. Login to azure via terminal by using `az login`
4. Create an .env file and insert your credentials.
    `cp .env.example .env`
5. If not already happen, init Terraform `terraform init`
6. [optional for deployment] Validate terraform `terraform validate`
7. apply Terraform on azure `bash apply_tf.bs`
8. Add Slack Informations to your App Configurations via Azure UI

__note__ I am using my personal tenant id instead of working with RBA
for my local setup and for git during this hackathon. For getting
your personal tenant id run `az login`. It will displays on the
response after login.
