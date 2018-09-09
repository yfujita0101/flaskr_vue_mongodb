<template>
  <!-- 表示画面 -->
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Posts</h1>
        <hr><br><br>
        <alert :message="message" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.post-modal>Add Posts</button>
        <br><br>
        <div class="card-columns">
          <div v-for="(post, index) in posts" :key="index"
                class="card border-primay mb-6" style="width: 18rem;">
            <div v-if="post.file_url">
              <img class="card-img-top" v-bind:src='post.file_url' alt="Card image cap">
            </div>
            <div class="card-header">{{ post.title }}</div>
            <div class="card-body text-primary">
              <div class="card-text" v-html="replaceReturn(post.body)"></div>
              <br/>
              <p class="card-text text-right">
                <small class="text-muted">
                  updated {{ post.updated | moment("YYYY/MM/DD HH:mm:ss")}}
                </small>
              </p>
              <div class="text-right">
                <button type="button"
                        class="btn btn-primary btn-sm"
                        v-b-modal.post-update-modal
                        @click="editPost(post)">
                  update
                </button>
                <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    @click="onDeletePost(post)">
                    delete
                  </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- add post modal -->
    <b-modal ref="addPostModal"
              id="post-modal"
              title="Add a new post"
              hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                      label="Title:"
                      label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addPostFrom.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-body-group"
                      label="Body:"
                      label-for="form-body-input">
          <b-form-textarea id="form-body-input"
                        v-model="addPostFrom.body"
                        required
                        placeholder="Enter content"
                        :rows="3"
                        :max-rows="6">
          </b-form-textarea>
        </b-form-group>
        <!-- image upload added -->
        <b-form-group id="form-file-group"
                      label="file:"
                      label-for="form-file-input">
          <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <!-- edit post modal -->
    <b-modal ref="editPostModal"
              id="post-update-modal"
              title="Update"
              hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group"
                      label="Title:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editPostForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-body-edit-group"
                      label="Body:"
                      label-for="form-body-edit-input">
            <b-form-textarea id="form-body-edit-input"
                          type="text"
                          v-model="editPostForm.body"
                          required
                          placeholder="Enter content"
                          :rows="3"
                          :max-rows="6">
            </b-form-textarea>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      posts: [],
      addPostFrom: {
        title: '',
        body: '',
        file: '',
      },
      editPostForm: {
        id: '',
        title: '',
        body: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPosts() {
      const path = 'http://localhost:5000/posts';
      axios.get(path)
        .then((res) => {
          this.posts = res.data.posts;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addPost(payload) {
      const path = 'http://localhost:5000/posts';
      // eslint-disable-next-line
      const config = {
        headers: {
          'content-type': 'multipart/form-data',
        },
      };
      axios.post(path, payload, config)
        .then(() => {
          this.getPosts();
          this.message = 'Post added';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getPosts();
        });
    },
    editPost(post) {
      this.editPostForm = post;
    },
    removePost(postID) {
      const path = `http://localhost:5000/posts/${postID}`;
      axios.delete(path)
        .then(() => {
          this.getPosts();
          this.message = 'Post removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getPosts();
        });
    },
    updatePost(payload, postID) {
      const path = `http://localhost:5000/posts/${postID}`;
      axios.put(path, payload)
        .then(() => {
          this.getPosts();
          this.message = 'Post updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getPosts();
        });
    },
    onDeletePost(post) {
      this.removePost(post.id);
    },
    initForm() {
      this.addPostFrom.title = '';
      this.addPostFrom.body = '';
      this.addPostFrom.file = '';
      this.editPostForm.id = '';
      this.editPostForm.title = '';
      this.editPostForm.body = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPostModal.hide();
      // eslint-disable-next-line
      let payload = new FormData();

      payload.append('title', this.addPostFrom.title);
      payload.append('body', this.addPostFrom.body);
      payload.append('file', this.addPostFrom.file);

      this.addPost(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPostModal.hide();
      const payload = {
        id: this.editPostForm.id,
        title: this.editPostForm.title,
        body: this.editPostForm.body,
      };
      this.updatePost(payload, this.editPostForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPostModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPostModal.hide();
      this.getPosts();
    },
    replaceReturn(str) {
      return str.replace(/\n/g, '<br />');
    },
    handleFileUpload() {
      this.addPostFrom.file = this.$refs.file.files[0];
    },
  },
  created() {
    this.getPosts();
  },
};
</script>
