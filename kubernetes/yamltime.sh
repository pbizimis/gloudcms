#!/bin/bash
kubectl apply -f cdn-backendconfig.yaml
kubectl apply -f philipbizimis-certificate.yaml
kubectl apply -f api-service.yaml
kubectl apply -f interface-service.yaml
kubectl apply -f db-service.yaml
kubectl apply -f db-storageclass.yaml
kubectl apply -f db-pvc.yaml
kubectl apply -f api-deployment.yaml
kubectl apply -f interface-deployment.yaml
kubectl apply -f db-deployment.yaml
kubectl apply -f ingress.yaml