#!/bin/bash
kubectl apply -f secrets.yaml
kubectl apply -f certificates.yaml
kubectl apply -f mongo.yaml
kubectl apply -f redis.yaml
kubectl apply -f interface.yaml
kubectl apply -f api.yaml
kubectl apply -f ingress.yaml