<template>
    <aside class="fixed left-0 top-14 h-screen w-60 bg-white  [&>h2]:font-semibold [&>h2]:py-2 [&>*]:px-2 [&>h2]:text-lg
     transition-transform duration-300 translate-x-0 z-50 border p-4
     ">
        <h2>Tags</h2>
        <div v-for="tab in tagsTabs" :key="tab.label" :class="[tabStyle]" @click="changeTab(tab.label, tab.route)">
            <i :class="[tab.myClass, 'pi text-sm']"></i>
            <p>{{ tab.label }}</p>
        </div>

        <h2>Documents</h2>
        <div v-for="tab in documentTabs" :key="tab.label" :class="[tabStyle]" @click="changeTab(tab.label, tab.route)">
            <i :class="[tab.myClass, 'pi text-sm']"></i>
            <p>{{ tab.label }}</p>
        </div>

        <h2>Settings</h2>
        <div v-for="tab in settingTabs" :key="tab.label" :class="[tabStyle]" @click="changeTab(tab.label, tab.route)">
            <i :class="[tab.myClass, 'pi text-sm']"></i>
            <p>{{ tab.label }}</p>
        </div>
    </aside>
    <div class="fixed inset-0 bg-black bg-opacity-50" hidden>

    </div>
</template>

<script setup>
import { ref, defineEmits, inject } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const route = useRoute()
const router = useRouter()
const emit = defineEmits(['change-tab']);
const currentTab = ref("Manage Tags");

const tabStyle =
    "px-4 font-semibold flex items-center gap-2 py-3 rounded text-[#555] hover:bg-[#EEF2FF] cursor-pointer hover:text-[#059862]";

const tagsTabs = [
    { label: "Manage Tags", myClass: "pi-tags", route: "/manage-tags" },
    { label: "Create New Tag", myClass: "pi-plus-circle", route: "/tags" },

];
const documentTabs = [
    { label: "My Documents", myClass: "pi-file", route: "/documents" },
    { label: "Modify Document", myClass: "pi-file-edit", route: "/update-document" },
]
const settingTabs = [
    { label: "Account", myClass: "pi-user", route: "/settings" },
];

const changeTab = (tabLabel, tabRoute) => {
    console.log(currentTab.value)
    currentTab.value = tabLabel;
    emit('change-tab', tabLabel);
    router.push(tabRoute)
};
</script>