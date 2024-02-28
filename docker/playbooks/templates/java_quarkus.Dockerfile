FROM maven:3.8.4-openjdk-17 AS build

WORKDIR /build
COPY ./pom.xml ./pom.xml
COPY ./settings.xml /root/.m2/settings.xml
RUN mvn dependency:go-offline -B

COPY src src
ARG QUARKUS_PROFILE
RUN mvn package -Dquarkus.profile=${QUARKUS_PROFILE}

FROM registry.access.redhat.com/ubi8/ubi-minimal:8.4

ARG JAVA_PACKAGE=java-17-openjdk-headless
ARG RUN_JAVA_VERSION=1.3.8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en'

# Install java and the run-java script
RUN microdnf install curl ca-certificates wget ${JAVA_PACKAGE} \
  && microdnf update \
  && microdnf clean all \
  && mkdir /deployments \
  && chown 1001 /deployments \
  && chmod "g+rwX" /deployments \
  && chown 1001:root /deployments \
  && curl https://repo1.maven.org/maven2/io/fabric8/run-java-sh/${RUN_JAVA_VERSION}/run-java-sh-${RUN_JAVA_VERSION}-sh.sh -o /deployments/run-java.sh \
  && chown 1001 /deployments/run-java.sh \
  && chmod 540 /deployments/run-java.sh \
  && echo "securerandom.source=file:/dev/urandom" >> /etc/alternatives/jre/conf/security/java.security

# We make four distinct layers so if there are application changes the library layers can be re-used
COPY --from=build /build/target/quarkus-app/lib/ /deployments/lib/
COPY --from=build /build/target/quarkus-app/*.jar /deployments/
COPY --from=build /build/target/quarkus-app/app/ /deployments/app/
COPY --from=build /build/target/quarkus-app/quarkus/ /deployments/quarkus/

USER 1001

ENTRYPOINT [ "/deployments/run-java.sh" ]
