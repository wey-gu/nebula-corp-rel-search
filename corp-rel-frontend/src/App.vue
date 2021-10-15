<template>
  <div id="app">
    <input v-model="entity" placeholder="Type An Entity, then Enter" v-on:keyup.enter="submit" />
    <network
      :nodeList="nodes"
      :linkList="relationships"
      :nodeSize="nodeSize"
      :linkWidth="linkWidth"
      :linkDistance="linkDistance"
      :linkTextFrontSize="linkTextFrontSize"
      :nodeTypeKey="nodeTypeKey"
      :linkTypeKey="linkTypeKey"
      :nodeTextKey="nodeTextKey"
      :linkTextKey="linkTextKey"
      :showNodeText="showNodeText"
      :showLinkText="showLinkText"
      >
    </network>
  </div>
</template>

<script>
import Network from "vue-network-d3";
import axios from "axios";

export default {
  name: "app",
  components: {
    Network
  },
  data() {
    return {
      entity: "",
      nodes: [
        {"id": "c_132", "name": "Chambers LLC", "tag": "corp"}],
      relationships: [],
      nodeSize: 18,
      linkDistance: 320,
      linkWidth: 6,
      linkTextFrontSize: 15,
      nodeTypeKey: "tag",
      linkTypeKey: "edge",
      nodeTextKey: "name",
      linkTextKey: "properties",
      showNodeText: true,
      showLinkText: true
    };
  },
  methods: {
    submit(e) {
      this.entity = e.target.value;
      let api_endpoint = "http://localhost:8081/api";
      axios
      .post(api_endpoint, { "entity": this.entity })
      .then(response => {
        console.log("Calling " + api_endpoint + " for " + this.entity);
        this.nodes = response.data.nodes;
        this.relationships = response.data.relationships;
        console.log(response.data.nodes);
        console.log(response.data.relationships);
      })
      .catch(err => console.log(err));
    }
  }
};
</script>

<style>
body {
  margin: 40;
}
input {
  width: 10%;
  text-align:center;
  padding: 12px 20px;
  margin: auto;
  box-sizing: border-box;
  margin-left: auto;
  margin-right: auto;
  vertical-align: middle;
  position: absolute;
  left: 45%;
  top: 10%;
}

</style>
