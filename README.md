# CryNet-K8s-Deployment Projesi

Bu proje, bir yapay zeka uygulamasının Docker ile konteynerize edilmesi, Kubernetes ile yönetilmesi ve CI/CD süreçlerinin otomatize edilmesini kapsayan bir Bulut Bilişim projesidir.

## Proje Görev Dağılımı

- **Murat Dahi (23010310025):** Uygulama Mimarisi, Docker Konteynerizasyonu, Python Flask uygulaması, Github Actions.
- **Yunus Emre Taşkesen (23010310067):** Kubernetes Mimarisi, GKE Cluster yönetimi, Manifest dosyaları.
- **Salih Unat (23010310078):** CI/CD Pipeline, Google Cloud Build entegrasyonu, Dokümantasyon.

## (Murat Dahi)

Projenin temel web uygulaması Python Flask ile geliştirilmiştir. Uygulamanın çalışma ortamı `Dockerfile` ile izole edilmiştir.

- **İmaj Adı:** `muratdahi/crynet-ai:version-1`
- **Port:** 8000
- **Model:** `crynet_model.pkl`

_Not: Yukarıda ki imaj ismi kullanilabilir._

## (Yunus Emre Taşkesen)

Bu bölümde, Dockerize edilmiş yapay zeka uygulamasının Google Kubernetes Engine (GKE) üzerinde ayağa kaldırılması, dış ağa açılması, veri kalıcılığının sağlanması 
ve ağ güvenliği süreçleri tasarlanmıştır. Altyapı, Kubernetes bildirim (manifest) dosyaları aracılığıyla "Kod Olarak Altyapı" (Infrastructure as Code) prensibiyle 
kurgulanmıştır.

**Geliştirilen Manifest Dosyaları:**

- **deployment.yaml:** Yapay zeka uygulamasının **(muratdahi/crynet-ai:version-1)** cluster içerisinde Pod'lar halinde çalışmasını sağlayan orkestrasyon
dosyasıdır. Uygulamanın 8000 portundan dinlenmesi ve kalıcı diskin (PVC) konteyner içindeki **/app/data** dizinine bağlanması (Volume Mount) bu mimaride
tanımlanmıştır.

- **service.yaml:** GKE üzerinde dış dünyadan erişilebilir statik bir External-IP sağlayan **LoadBalancer** servisidir. Gelen standart web trafiğini (Port 80),
içeride çalışan Flask uygulamasının dinlediği hedefe (TargetPort 8000) yönlendirir.

- **pvc.yaml:** Projenin durum bilgisi (Stateful) gereksinimlerini karşılamak üzere **ReadWriteOnce** erişim modunda yapılandırılmış Kalıcı Depolama Alanı
(Persistent Volume Claim) manifestosudur.

- **networkpolicy.yaml:** Küme içerisindeki Pod'ların ağ trafiğini sınırlandıran güvenlik kalkanıdır. Zero Trust mantığıyla, Ingress (giriş) trafiğine sadece
uygulamanın çalıştığı 8000 portu üzerinden izin verilmiştir.


**Sistem Operasyonları ve Hata Yönetimi:**

- **Ölçekleme (Scaling):** Sistem yüküne göre sunucu kaynaklarının **kubectl scale** komutlarıyla manuel olarak artırılıp azaltılması test edilmiştir.

- Rolling Update ve Rollback: Uygulamanın yeni versiyonlarının sıfır kesinti (Zero Downtime) ile canlıya alınması sağlanmıştır. Olası bir sürüm hatasında **kubectl
rollout** undo komutuyla saniyeler içinde stabil sürüme geri dönme senaryoları tasarlanmış ve doğrulanmıştır.

- **Deadlock Çözümü: ReadWriteOnce** kuralına sahip kalıcı disklerin Rolling Update veya Scaling sırasında yaratabileceği kilitlenme (ContainerCreating durumunda
takılı kalma) senaryoları analiz edilmiş ve "Scale to Zero" mantığıyla operasyonel çözümler sisteme entegre edilmiştir.

## (Salih Unat)

Projenin sürekli entegrasyon (CI), sürekli dağıtım (CD), bulut altyapı yönetimi ve sistem entegrasyonu süreçleri yürütülmüştür. Proje kapsamında gerçekleştirilen teknik adımlar şunlardır:

- **CI/CD Pipeline Yapılandırması:** Projenin tam otomatik dağıtım süreçleri için **Google Cloud Build** entegrasyonu gerçekleştirilmiş ve `cloudbuild.yaml` boru hattı mimarisi sıfırdan tasarlanmıştır. GitHub ana branch'ine yapılan her `push` işleminin sistemi otomatik tetiklemesi sağlanmıştır.
- **IAM ve Güvenlik Yetkilendirmeleri:** Cloud Build servis hesabına GKE üzerinde güvenli dağıtım yapabilmesi için `Kubernetes Engine Developer` rolü atanmıştır. Servis hesabı yetki sınırlarından kaynaklanan loglama blokajı, pipeline mimarisine `options: logging: CLOUD_LOGGING_ONLY` konfigürasyonu entegre edilerek çözülmüştür.
- **Dinamik Manifesto Yamalama (Automated Patching):** Boru hattı üzerine entegre edilen `sed` betikleri vasıtasıyla, Kubernetes `deployment.yaml` dosyasındaki taslak `nginx:latest` imaj alanı Artifact Registry'deki benzersiz sürüm etiketiyle (`SHORT_SHA`) dinamik olarak değiştirilmiş ve container portu uygulamanın asıl çalışma portu olan `8000` ile otomatik eşitlenmiştir.
- **Altyapı Dağıtımı ve GKE Yönetimi:** Küme kaynaklarını ve bütçeyi optimize etmek amacıyla `us-central1` bölgesinde **GKE Autopilot** kümesi (`crynet-cluster`) ayağa kaldırılmıştır. Pipeline dağıtım adımında tekil dosya yerine tüm klasör hedeflenerek; `deployment.yaml`, `service.yaml`, `pvc.yaml` ve `networkpolicy.yaml` nesnelerinin cluster üzerine eşzamanlı ve bağımlılık hatası olmadan kurulması sağlanmıştır.
- **Ağ Güvenliği ve Port Çözümlemesi (Troubleshooting):** Canlı dağıtım sonrasında LoadBalancer dış IP'sinin uygulamaya erişememesi sorunu analiz edilmiş; `networkpolicy.yaml` dosyasında yer alan ingress kısıtlamasının pod içi `port: 80` yerine uygulamanın asıl yayın yaptığı `port: 8000` (FastAPI) kapısına çekilmesi sağlanarak ağ blokajı tamamen çözülmüş ve sistem kesintisiz olarak dış dünyaya açılmıştır.

### Proje Teknik Özeti
* **Kullanılan CI/CD Aracı:** Google Cloud Build (Jenkins alternatifi sunucusuz bulut çözümü)
* **Canlı Altyapı:** Google Kubernetes Engine (GKE) Autopilot - 3 Aktif Node
* **Üretim Ortamı Dış IP Adresi:** http://35.225.10.205 (Port 80 HTTP karşılaması, Port 8000 TargetPort yönlendirmesi)
