

## Ollama

## ollama -v
Ollama version

## ollama run llama3.2
run CLI

## curl command hit API endpoint
curl --noproxy "*" http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt":"Why is the sky blue?"
}'

## check ollama process
ps aux | grep -E 'ollama'


## nvidia-smi
Show nvidia driver, CUDA version, processes _etc._


# Docker

## docker run hello-world
run test container  

## docker ps
show running containers

## start container - yaml uses .env for info
docker-compose -f /mnt/c/free-genai-bootcamp-2025/opea-comps/docker-componse.yaml up

## check Docker health
curl http://localhost:11434/health



## adding to compose file - not working
      /bin/sh -c "ollama pull llama3.2 && ollama run"

## up / down
docker-compose -f /mnt/c/free-genai-bootcamp-2025/opea-comps/docker-componse.yaml down
docker-compose -f /mnt/c/free-genai-bootcamp-2025/opea-comps/docker-componse.yaml up

## ask LLM in Docker with curl


## docker setup nvidia
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker



curl --noproxy "*" http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt":"Why is the sky blue?"
}'