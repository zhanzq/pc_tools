

# maven使用指南

## 1. maven配置常见问题
maven使用过程中，经常出现一些问题，大部分可以通过配置进行解决。

### 1.1 Maven 3.8.1 blocked mirrors "fix"

This is not a fix, but a workaround for repositories not on HTTPS yet. Use with caution.

Error
[ERROR] (...) Could not transfer artifact no.whatever:whatever-client:pom:3.1 from/to maven-default-http-blocker (http://0.0.0.0/): Blocked mirror for repositories: [releases (http://unportected.com/nexus/content/repositories/releases, defaul)] -> [Help 1]
"Fix"
Put this section in your

`~/.m2/settings.xml`

-file, and rerun mvn with -U option.

具体代码如下：
```xml
    <mirrors>
        <mirror>
            <id>maven-default-http-blocker</id>
            <mirrorOf>external:dont-match-anything-mate:*</mirrorOf>
            <name>ANYTHING YOU WANT</name>
            <url>http://0.0.0.0/</url>
            <blocked>false</blocked>
        </mirror>
    </mirrors>
```
