# TiktokDouyinCrawler
国外Tiktok+国内抖音评论爬虫，
msToken、ttwid、webid、a-bogus和x-bogus算法破解

## 注意
源码仅作为和大家一起**学习Python**使用，你可以免费: 拷贝、分发和派生当前源码。

但你用于*商业目的*及其他*恶意用途*，作者也不会管你，耗子尾汁

> 项目普及技术：JS逆向（调用JS文件） 

> 最好使用代理IP爬取，最近发现Tiktok屏蔽香港的IP，代理国外IP最好用美国的

## x-bogus
x-bogus是一种防数据包伪造的一个参数， 又称为x伪造，主要用于反爬虫，这个是某节公司下面基础服务，这个反爬虫机制几乎用在了它所有的产品中，不过，只要是能正常使用，这些东西都是透明的，x-bogus生成算法。

## a-bogus
同x-bogus，x-bogus的新版本

## msToken
msToken可以理解成Message Token，相当于每次消息请求的令牌，主要用于请求统计，这也是具有反爬虫的机制，如果相同msToken请求太多，也会被定义成恶意请求，这时候会出现验证码校验。所以我们在使用的时候，可以用uuid或者是雪花算法的id来模拟msToken，当然长度大于32位的唯一串最好

## ttwid
ttwid类似客户端id，即便是游客模式，也可以对页面数据进行埋点统计，通过收集ttwid下的用户行为数据，给与内容推荐和广告推荐。这个也是某节公司下的基础服务，所以生成的id，只要是某节下的服务都可以使用

## webid
同ttwid，类似客户端id，也可以说是浏览器id，不过ttwid可在cookie获取，webid可在随意一个视频请求，返回的html文本的script里再通过正则获取

## 详细讲解可阅读
https://blog.csdn.net/u013444182/article/details/134933150

## 爬取如下：
<img src="https://raw.githubusercontent.com/NearHuiwen/TiktokDouyinCrawler/main/img/img1.png">

