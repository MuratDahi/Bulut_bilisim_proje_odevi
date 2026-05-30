# CryNet-K8s-Deployment Projesi

Bu proje, bir yapay zeka uygulamasının Docker ile konteynerize edilmesi, Kubernetes ile yönetilmesi ve CI/CD süreçlerinin otomatize edilmesini kapsayan bir Bulut Bilişim projesidir.

## Proje Görev Dağılımı

- **Murat Dahi (23010310025):** Uygulama Mimarisi, Docker Konteynerizasyonu, Python Flask uygulaması, Github Actions.
- **Yunus Emre Taşkesen (23010310067):** Kubernetes Mimarisi, GKE Cluster yönetimi, Manifest dosyaları.
- **Salih Unat (23010310078):** CI/CD Pipeline, Google Cloud Build entegrasyonu, Dokümantasyon.

## (Murat Dahi)

Projenin temel web uygulaması Python Flask ile geliştirilmiştir. Uygulamanın çalışma ortamı `Dockerfile` ile izole edilmiştir.

- **İmaj Adı:** `MuratDahi/crynet-ai:version-1`
- **Port:** 8000
- **Model:** `crynet_model.pkl`

_Not: Yukarıda ki imaj ismi kullanilabilir._
