# Instructions for Starting the Project
 

First set environment variables for database  

     export PG_DB=your_database_name
     export PG_USER=your_username
     export PG_PASSWORD=your_password

Simple run with docker compose [v2.*]
`docker compose up`

# Test
 `pytest tests/`
 



# K8s
name of k8s cluster: **demo-eks**




## Install and Configure AWS EBS CSI Driver
To enable volume management with the AWS EBS CSI driver in your Kubernetes cluster, follow these steps:

1. **Add the EBS CSI Driver Helm repository and update**:
   Run the following command to add the repository and update the Helm chart index:
   ```sh
   helm repo add ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver &
   helm repo update
   
2. **Install the EBS CSI driver in the kube-system**:
   Run the following command:
   ```sh
   helm install ebs-csi-driver ebs-csi-driver/aws-ebs-csi-driver --namespace kube-system --create-namespace
   
3. **[Temporary] Create aws policy and attach to ***eks-demo-node*** role**:
  `{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": [
"ec2:AttachVolume",
"ec2:CreateVolume",
"ec2:DescribeVolumes",
"ec2:DeleteVolume",
"ec2:ModifyVolume",
"ec2:DetachVolume",
"ec2:DescribeAvailabilityZones",
"ec2:CreateTags",
"ec2:DescribeVolumeStatus"
],
"Resource": "*"
}
]
}`

4. **Install nginx ingress controller**:
   ```sh
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

5. **Install application:**
  ```sh
  helm install [name] -n prod ./crypto-arp-tracker