# Template Matching ile Drone Tespiti

Bu proje, bilgisayarlı görü dersi kapsamında **Şablon Eşleştirme (Template Matching)** yöntemi kullanılarak geliştirilmiş bir **drone tespit sistemi**dir. Projenin amacı, görüntülerde drone bulunup bulunmadığını tespit etmek ve drone bulunduğunda konumunu yeterli doğrulukla belirlemektir.

Şablon eşleştirme işlemi için OpenCV kütüphanesinin `matchTemplate()` fonksiyonu ve **TM_CCOEFF_NORMED** yöntemi kullanılmıştır. Bu yöntem, normalizasyon işlemi sayesinde farklı parlaklık seviyelerine sahip görüntülerde daha kararlı sonuçlar vermesi nedeniyle tercih edilmiştir. Eşleştirme sonucu **-1 ile 1** arasında değer almaktadır. **1'e yakın değerler** yüksek benzerliği, **0 civarındaki değerler** düşük ilişkiyi, negatif değerler ise negatif korelasyonu ifade etmektedir. Bu nedenle model, 1'e yakın eşleştirme skorlarını olası drone tespitleri olarak değerlendirmektedir.

## Görüntü Ön İşleme

Model geliştirilmeden önce görüntülere aşağıdaki ön işlemler uygulanmıştır:

* Görüntüler gri tonlamaya dönüştürülmüştür.
* Tüm görüntüler **256×256** boyutuna yeniden ölçeklendirilmiştir.
* Eğitim veri setindeki drone görüntüleri şablon olarak kullanılmıştır.
* Farklı drone boyutlarını tespit edebilmek amacıyla şablonlar **çoklu ölçeklerde (multi-scale)** değerlendirilmiştir.

## Model Geçerleme ve Eşik Optimizasyonu

`validation.ipynb` dosyasında bulunan `validate_model()` fonksiyonu kullanılarak model, aynı validation veri seti üzerinde **10 farklı eşik değeri** ile ayrı ayrı değerlendirilmiştir.

Değerlendirme sırasında:

* Görüntüde drone yoksa ve model doğru şekilde **"drone yok"** tahmini yaparsa başarılı kabul edilmiştir.
* Görüntüde drone varsa modelin drone'u tespit etmesi ve tahmin edilen bölgenin gerçek bounding box ile **IoU ≥ %50** değerine sahip olması başarılı tahmin olarak kabul edilmiştir.
* Bu şartları sağlamayan tahminler başarısız olarak değerlendirilmiştir.

Her eşik değeri için:

* **Precision**
* **Recall**
* **F1-Score**
* **Accuracy**
* **Karmaşıklık Matrisi (Confusion Matrix)**

hesaplanarak modelin performansı analiz edilmiştir.

Yapılan geçerleme sonucunda, farklı eşik değerleri arasından **F1-Score baz alınarak en uygun eşik değerinin 0.465 olduğu** belirlenmiştir.

## Kullanılan Teknolojiler

* **Python**
* **OpenCV**
* **NumPy**
* **Scikit-Learn**
* **Matplotlib**

**Yöntem:** Multi-Scale Template Matching (`TM_CCOEFF_NORMED`)
**Problem:** Drone Tespiti
**Optimal Eşik Değeri:** `0.465`


## Rapor

Projenin veri seti, yöntem, algoritma, hiperparametreler, geçerleme sonuçları, performans metrikleri, karmaşıklık matrisleri ve elde edilen sonuçlar hakkında **daha detaylı bilgi için `Rapor.pdf` dosyasına başvurabilirsiniz**.
