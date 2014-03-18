<?xml version="1.0"?>
<recipe>
    <instantiate from="AndroidManifest.xml.ftl" />

<#if copyIcons>
    <copy from="res/drawable-hdpi" />
    <copy from="res/drawable-mdpi" />
    <copy from="res/drawable-xhdpi" />
</#if>
    <copy from="res/values/styles.xml" />
<#if buildApi gte 11>
    <copy from="res/values-v11/styles.xml" />
</#if>
<#if buildApi gte 14>
    <copy from="res/values-v14/styles.xml" />
</#if>

    <instantiate from="res/values/strings.xml.ftl" />
</recipe>
