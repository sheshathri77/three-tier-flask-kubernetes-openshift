# Three-Tier Flask Web Application – Docker, Kubernetes & OpenShift

A containerized three-tier To-Do web application deployed using Docker, Kubernetes (Minikube), and Red Hat OpenShift.

This project demonstrates containerization, microservice communication, Kubernetes orchestration, application networking, persistent storage, access control, and container security.

## Project Overview

The application follows a three-tier architecture:

1. **Presentation Layer:** Flask-based frontend that displays and manages To-Do tasks.
2. **Application Layer:** Flask backend API that handles task operations and business logic.
3. **Database Layer:** MySQL database that stores application data.

Nginx acts as a reverse proxy, routing incoming requests to the appropriate application service.

## Architecture

```text
                   User / Browser
                         |
                         v
                  Nginx Reverse Proxy
                     Port 80
                         |
             +-----------+-----------+
             |                       |
             v                       v
       Frontend (Flask)         Backend API
         Port 8000              Port 4000
             |                       |
             |                       v
             +----------------> MySQL Database
                                   Port 3306
```

### Request Flow

- The user accesses the application through the Nginx endpoint.
- Nginx forwards page requests to the frontend.
- The frontend communicates with the backend API to retrieve task information.
- The backend communicates with MySQL to create, retrieve, update, and delete tasks.
- The frontend displays the results to the user.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python / Flask | Frontend and backend application |
| MySQL 8.0 | Relational database |
| SQLAlchemy | Database interaction |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes environment |
| kubectl | Kubernetes management |
| Nginx | Reverse proxy |
| YAML | Infrastructure configuration |
| OpenShift | Enterprise Kubernetes platform |
| oc CLI | OpenShift management |

## Repository Structure

```text
three-tier-flask-kubernetes-openshift/
│
├── ApplicationLayer/
│   ├── app.py
│   ├── parameters.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── WebLayer/
│   ├── app.py
│   ├── templates/
│   ├── requirements.txt
│   └── Dockerfile
│
├── cfn-stacks/
│   └── AWS CloudFormation templates
│
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── mysql-deployment.yaml
│   ├── mysql-pvc.yaml
│   ├── mysql-service.yaml
│   ├── nginx-deployment.yaml
│   ├── nginx-service.yaml
│   ├── web-deployment.yaml
│   ├── web-service.yaml
│   ├── ingress.yaml
│   ├── web-network-policy.yaml
│   ├── web-security-patch.yaml
│   ├── todo-viewer-role.yaml
│   └── todo-viewer-binding.yaml
│
├── nginx/
│   └── default.conf
│
├── openshift/
│   ├── nginx.conf
│   ├── nginx-network-policy.yaml
│   └── nginx-service-patch.yaml
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

## 1. Run the Application Using Docker Compose

### Prerequisites

- Docker Desktop
- Git

### Clone the Repository

```bash
git clone https://github.com/sheshathri77/three-tier-flask-kubernetes-openshift.git

cd three-tier-flask-kubernetes-openshift
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=mysql:3306
DB_NAME=tododb
```

Use the database values expected by your Docker Compose and MySQL configuration.

**Security:** Never commit `.env` to GitHub.

### Build and Start Containers

```bash
docker compose up -d --build
```

### Verify Containers

```bash
docker compose ps
```

### Access the Application

Open:

```text
http://localhost:8080
```

### View Container Logs

```bash
docker compose logs -f
```

### Stop Containers

```bash
docker compose down
```

To remove the database volume as well, use `docker compose down -v`. Warning: this deletes the persisted MySQL data.

## 2. Deploy Using Kubernetes (Minikube)

### Prerequisites

- Docker Desktop
- Minikube
- kubectl

### Start Minikube

```bash
minikube start
```

Check the cluster:

```bash
kubectl cluster-info
kubectl get nodes
```

### Create the Namespace

```bash
kubectl create namespace todo-app
```

### Create Configuration and Secret Resources

The Kubernetes manifests refer to a ConfigMap named `mysql-config` and a Secret named `mysql-secret`.

Create the ConfigMap:

```bash
kubectl create configmap mysql-config \
  --from-literal=MYSQL_DATABASE=tododb \
  -n todo-app
```

Create the Secret using your actual database credentials:

```bash
kubectl create secret generic mysql-secret \
  --from-literal=MYSQL_ROOT_PASSWORD='YOUR_ROOT_PASSWORD' \
  --from-literal=MYSQL_USER='YOUR_DATABASE_USER' \
  --from-literal=MYSQL_PASSWORD='YOUR_DATABASE_PASSWORD' \
  -n todo-app
```

Replace the example values with your own credentials. Do not put real credentials in YAML files committed to GitHub.

The RoleBinding also requires the `todo-viewer` ServiceAccount:

```bash
kubectl create serviceaccount todo-viewer -n todo-app
```

### Build Application Images

Build the backend and frontend images in Minikube's Docker environment:

```bash
minikube image build -t three-tier-web-application-flask-backend:latest ./ApplicationLayer

minikube image build -t three-tier-web-application-flask-web:latest ./WebLayer
```

### Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/
```

### Verify Kubernetes Resources

```bash
kubectl get pods -n todo-app
kubectl get deployments -n todo-app
kubectl get services -n todo-app
kubectl get pvc -n todo-app
kubectl get ingress -n todo-app
```

### Access the Application

The Nginx Service is configured as a NodePort on port `30080`.

```bash
minikube service nginx -n todo-app
```

### Check Deployment Rollout History

```bash
kubectl rollout history deployment/web -n todo-app
```

### Perform a Rollback

```bash
kubectl rollout undo deployment/web -n todo-app
```

Verify the rollback:

```bash
kubectl rollout status deployment/web -n todo-app
```

## 3. OpenShift Deployment

The `openshift/` directory contains OpenShift-specific Nginx configuration and supporting network-policy and Service patch YAML files.

### Prerequisites

- Access to an OpenShift cluster
- OpenShift CLI (`oc`)

### Login to OpenShift

```bash
oc login <OPENSHIFT_API_URL>
```

### Select Your Project

```bash
oc project <PROJECT_NAME>
```

### Verify Application Resources

```bash
oc get deployments
oc get pods
oc get services
oc get routes
```

### Verify Pod Security Constraints

```bash
oc get pod <POD_NAME> -o yaml
```

Check the Pod annotation:

```text
openshift.io/scc: restricted-v2
```

OpenShift's `restricted-v2` SCC provides security restrictions for application containers, including non-root execution and restricted privileges.

**Note:** The files in `openshift/` are supporting configuration and patch files, not a complete standalone OpenShift deployment. They must be applied in the context of the corresponding OpenShift resources.

## 4. Kubernetes Security and Administration

The project includes examples of Kubernetes security and administration.

### ConfigMaps

Used to store non-sensitive application configuration separately from container images.

### Secrets

Used to supply sensitive configuration such as database passwords.

### RBAC

A Role and RoleBinding provide the `todo-viewer` ServiceAccount with permission to get, list, and watch Pods.

### Network Policies

A NetworkPolicy is configured to control traffic to the frontend Pods.

Actual policy enforcement depends on the Kubernetes network plugin.

### Pod Security Context

The frontend security patch configures the container to run as a non-root user, disables privilege escalation, and drops Linux capabilities.

### Persistent Storage

A PersistentVolumeClaim provides persistent storage for MySQL data.

## 5. Useful Commands

| Task | Command |
|---|---|
| List Pods | `kubectl get pods -n todo-app` |
| List Deployments | `kubectl get deployments -n todo-app` |
| List Services | `kubectl get services -n todo-app` |
| Describe a Pod | `kubectl describe pod <POD_NAME> -n todo-app` |
| View logs | `kubectl logs <POD_NAME> -n todo-app` |
| Check rollout | `kubectl rollout status deployment/web -n todo-app` |
| View rollout history | `kubectl rollout history deployment/web -n todo-app` |
| Rollback | `kubectl rollout undo deployment/web -n todo-app` |
| Check ConfigMaps | `kubectl get configmaps -n todo-app` |
| Check Secrets | `kubectl get secrets -n todo-app` |
| Check PVCs | `kubectl get pvc -n todo-app` |

## Learning Outcomes

Through this project, I gained practical experience with:

- Designing a three-tier application architecture.
- Containerizing Flask applications using Docker.
- Running multi-container applications using Docker Compose.
- Deploying applications using Kubernetes.
- Managing Kubernetes Deployments, Services, and Ingress.
- Configuring ConfigMaps, Secrets, and persistent storage.
- Implementing RBAC and Pod security configurations.
- Working with Nginx reverse proxy configurations.
- Managing application deployments in OpenShift.
- Performing Kubernetes rollout updates and rollbacks.
- Troubleshooting container and application deployment issues.

## Author

**Sheshathri**

GitHub: https://github.com/sheshathri77

Project Repository: https://github.com/sheshathri77/three-tier-flask-kubernetes-openshift

---

*This project is based on the AWS Samples Three-Tier Flask Web Application, with additional Docker, Kubernetes, and OpenShift implementation and configuration work.*
