<template>
  <!-- 表示画面 -->
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Posts</h1>
        <hr><br><br>
        <alert :message="message" v-if="showMessage"></alert>
        <alert :message="message" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm">Add Posts</button>
        <br><br>
        <div class="card-deck">
          <div v-for="(post, index) in posts" :key="index"
                class="card border-primay mb-3" style="width: 18rem;">
            <div class="card-header">{{ post.title }}</div>
            <div class="card-body text-primary">
              <p class="card-text">{{ post.body }}</p>
              <div class="text-right">
                <a href="#" class="btn btn-primary">update</a>
                <a href="#" class="btn btn-warning">delete</a>
              </div>
              <p class="card-text text-right">
                <small class="text-muted">
                  updated {{ post.updated | moment("YYYY/MM/DD hh:mm:ss")}}
                </small>
              </p>
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
          <b-form-input id="form-body-input"
                        type="text"
                        v-model="addPostFrom.body"
                        required
                        placeholder="Enter content">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
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
      axios.post(path, payload)
        .then((res) => {
          this.getPosts();
          this.message = 'Post added';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getPosts();
        });
    },
    initForm() {
      this.addPostFrom.title = '';
      this.addPostFrom.body = '';
    }
  },
  created() {
    this.getPosts();
  },
};

</script>
