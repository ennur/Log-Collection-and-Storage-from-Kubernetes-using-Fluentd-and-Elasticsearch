# Log-Collection-and-Storage-from-Kubernetes-using-Fluentd-and-Elasticsearch

## Kind ile Cluster Oluşturma (3 nodes)

- "kind-k8s" klasöründe bulunan kind.config.yml dosyası çalıştırılır

## Docker ile Elasticsearch Server Oluşturma

- "elasticsearch" klasöründeki docker-compose.yml dosyası çalıştırılır.

Ardından şu komut çalıştırılır. (Bu komut "fluentd" klasöründe bulunan "Dockerfile" ve "fluent.conf" dosyaları içindir.)

```python
docker-compose up --detach
```


## Fluentd ile Logları Toplama ve Elasticsearch'de Depolama

* "fluentd" klasöründeki "fluentd.yml" çalıştırılır. Not: "deployment" logları test etmek için kullanılan uygulama olarak kullanıldı.

* NOT: Burada çalıştırmadan önce "Daemonset" de bulunan aşağıdaki kısmın bilgisayarın IPsi ile değişmesi gerekir.
  
  ```python
   env:
        - name: FLUENTD_HOST
          value: "192.168.117.23" #YOUR FLUENTD HOST IP
  ```

* Kibanadan, management->index management-> create-> fluentd* -> next -> @timestamp olarak text field ayarlanır


## Logların Sorgusu için Uygulama

* Dockerfile derlenmeden önce "main.py" dosyasındaki aşağıdaki satırda bulunan ipnin yine bilgisayarın IPsi ile değişmesi gerekir. 
  
  Not: Biz "wlo1" daki IP'yi kullandık.

* "main" klasöründeki "Dockerfile" derlenir.Örnek derleme:
  ```python
  docker build -t my-app:latest .
  
  ```
* Ardından uygulamanın k8sde çalışabilmesi için şu komut çalıştırılır.

```python
kind load docker-image my-app:latest --name "k8s-playground" 
```


## Logları Test Etmek için Uygulama

* "fluentd" klasöründeki "fluentd.yml" içerisindeki "Deployment" kullanıldı. 



## Logların Sorgulayan Uygulamanın K8S'de Çalıştırılması

* ""kind-k8s" klasöründe bulunan "app.yml" ve "endpoint.yml" çalıştırılır.

* Bu dosyalar çalıştırılmadan önce şunlara dikkat edilir:
  - "app.yml" dosyası içerisinde bulunan "image" adı build edilenle uyuşması gerekir.
  - Yukarıdakilere benzer şekilde "endpoint.yml" dosyasının içerisinde bulanan aşağıdaki satıra, bilgisayarın IPsinin yazılıması gerekir.

  ```python
  subsets:
  - addresses:
      - ip: 192.168.2.27 
  ```


## Uygulamanın Kullanımı

* IP adresini bulmak için şu komut çalıştırılır.
  
  ```python
  kubectl logs app
  ```
```python
http://<ip>:5000/kubernetes.labels.name/app

```
* Url deki "kubernetes.labels.name" ve "app" istenilen sorguya göre değişebilir.

* Örneğin, namespace'i kube-system olan loglar
  
 ```python
 http://<ip>:5000/kubernetes.namespace_name/kube-system
 
 ```
* Ayrıca zaman araması için aşağıdaki komut kullanılabilir.
  
  ```python
 http://<ip>:5000/@timestamp/2021-10-15
 
 ```

 DipNot: "http://<ip>:5000/" sadece bu url ile "Not Found" bilgisi döndürür. Parametre vermek gerekir.
