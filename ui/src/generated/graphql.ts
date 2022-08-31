import gql from 'graphql-tag';
import * as Urql from 'urql';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  DateTime: any;
};

export type Image = Node & {
  __typename?: 'Image';
  createdOn?: Maybe<Scalars['DateTime']>;
  filename?: Maybe<Scalars['String']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  requestId?: Maybe<Scalars['Int']>;
  selected?: Maybe<Scalars['Boolean']>;
  taskId?: Maybe<Scalars['Int']>;
  updatedOn?: Maybe<Scalars['DateTime']>;
};

export type ImageConnection = {
  __typename?: 'ImageConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<ImageEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
};

/** A Relay edge containing a `Image` and its cursor. */
export type ImageEdge = {
  __typename?: 'ImageEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<Image>;
};

/** An enumeration. */
export enum ImageSortEnum {
  CreatedOnAsc = 'CREATED_ON_ASC',
  CreatedOnDesc = 'CREATED_ON_DESC',
  FilenameAsc = 'FILENAME_ASC',
  FilenameDesc = 'FILENAME_DESC',
  IdAsc = 'ID_ASC',
  IdDesc = 'ID_DESC',
  RequestIdAsc = 'REQUEST_ID_ASC',
  RequestIdDesc = 'REQUEST_ID_DESC',
  SelectedAsc = 'SELECTED_ASC',
  SelectedDesc = 'SELECTED_DESC',
  TaskIdAsc = 'TASK_ID_ASC',
  TaskIdDesc = 'TASK_ID_DESC',
  UpdatedOnAsc = 'UPDATED_ON_ASC',
  UpdatedOnDesc = 'UPDATED_ON_DESC'
}

/** An object with an ID */
export type Node = {
  /** The ID of the object. */
  id: Scalars['ID'];
};

/** The Relay compliant `PageInfo` type, containing data necessary to paginate this connection. */
export type PageInfo = {
  __typename?: 'PageInfo';
  /** When paginating forwards, the cursor to continue. */
  endCursor?: Maybe<Scalars['String']>;
  /** When paginating forwards, are there more items? */
  hasNextPage: Scalars['Boolean'];
  /** When paginating backwards, are there more items? */
  hasPreviousPage: Scalars['Boolean'];
  /** When paginating backwards, the cursor to continue. */
  startCursor?: Maybe<Scalars['String']>;
};

export type Query = {
  __typename?: 'Query';
  allImages?: Maybe<ImageConnection>;
  allRequests?: Maybe<RequestConnection>;
  allTasks?: Maybe<TaskConnection>;
  node?: Maybe<Node>;
};


export type QueryAllImagesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  sort?: InputMaybe<Array<InputMaybe<ImageSortEnum>>>;
};


export type QueryAllRequestsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  sort?: InputMaybe<Array<InputMaybe<RequestSortEnum>>>;
};


export type QueryAllTasksArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  sort?: InputMaybe<Array<InputMaybe<TaskSortEnum>>>;
};


export type QueryNodeArgs = {
  id: Scalars['ID'];
};

export type Request = Node & {
  __typename?: 'Request';
  approved?: Maybe<Scalars['Boolean']>;
  createdOn?: Maybe<Scalars['DateTime']>;
  generated?: Maybe<Scalars['Boolean']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  images?: Maybe<ImageConnection>;
  kind: Scalars['String'];
  priority?: Maybe<Scalars['Int']>;
  prompt: Scalars['String'];
  tasks?: Maybe<TaskConnection>;
  updatedOn?: Maybe<Scalars['DateTime']>;
};


export type RequestImagesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
};


export type RequestTasksArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
};

export type RequestConnection = {
  __typename?: 'RequestConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<RequestEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
};

/** A Relay edge containing a `Request` and its cursor. */
export type RequestEdge = {
  __typename?: 'RequestEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<Request>;
};

/** An enumeration. */
export enum RequestSortEnum {
  ApprovedAsc = 'APPROVED_ASC',
  ApprovedDesc = 'APPROVED_DESC',
  CreatedOnAsc = 'CREATED_ON_ASC',
  CreatedOnDesc = 'CREATED_ON_DESC',
  GeneratedAsc = 'GENERATED_ASC',
  GeneratedDesc = 'GENERATED_DESC',
  IdAsc = 'ID_ASC',
  IdDesc = 'ID_DESC',
  KindAsc = 'KIND_ASC',
  KindDesc = 'KIND_DESC',
  PriorityAsc = 'PRIORITY_ASC',
  PriorityDesc = 'PRIORITY_DESC',
  PromptAsc = 'PROMPT_ASC',
  PromptDesc = 'PROMPT_DESC',
  UpdatedOnAsc = 'UPDATED_ON_ASC',
  UpdatedOnDesc = 'UPDATED_ON_DESC'
}

export type Task = Node & {
  __typename?: 'Task';
  createdOn?: Maybe<Scalars['DateTime']>;
  error?: Maybe<Scalars['String']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  images?: Maybe<ImageConnection>;
  kind: Scalars['String'];
  priority?: Maybe<Scalars['Int']>;
  requestId?: Maybe<Scalars['Int']>;
  running?: Maybe<Scalars['Boolean']>;
  status: Scalars['String'];
  updatedOn?: Maybe<Scalars['DateTime']>;
  workerId: Scalars['String'];
};


export type TaskImagesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
};

export type TaskConnection = {
  __typename?: 'TaskConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<TaskEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
};

/** A Relay edge containing a `Task` and its cursor. */
export type TaskEdge = {
  __typename?: 'TaskEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<Task>;
};

/** An enumeration. */
export enum TaskSortEnum {
  CreatedOnAsc = 'CREATED_ON_ASC',
  CreatedOnDesc = 'CREATED_ON_DESC',
  ErrorAsc = 'ERROR_ASC',
  ErrorDesc = 'ERROR_DESC',
  IdAsc = 'ID_ASC',
  IdDesc = 'ID_DESC',
  KindAsc = 'KIND_ASC',
  KindDesc = 'KIND_DESC',
  PriorityAsc = 'PRIORITY_ASC',
  PriorityDesc = 'PRIORITY_DESC',
  RequestIdAsc = 'REQUEST_ID_ASC',
  RequestIdDesc = 'REQUEST_ID_DESC',
  RunningAsc = 'RUNNING_ASC',
  RunningDesc = 'RUNNING_DESC',
  StatusAsc = 'STATUS_ASC',
  StatusDesc = 'STATUS_DESC',
  UpdatedOnAsc = 'UPDATED_ON_ASC',
  UpdatedOnDesc = 'UPDATED_ON_DESC',
  WorkerIdAsc = 'WORKER_ID_ASC',
  WorkerIdDesc = 'WORKER_ID_DESC'
}

export type AllRequestsQueryVariables = Exact<{
  sort?: InputMaybe<Array<InputMaybe<RequestSortEnum>> | InputMaybe<RequestSortEnum>>;
}>;


export type AllRequestsQuery = { __typename?: 'Query', allRequests?: { __typename?: 'RequestConnection', edges: Array<{ __typename?: 'RequestEdge', node?: { __typename?: 'Request', id: string, prompt: string, priority?: number | null, approved?: boolean | null, generated?: boolean | null, kind: string, createdOn?: any | null, updatedOn?: any | null, tasks?: { __typename?: 'TaskConnection', edges: Array<{ __typename?: 'TaskEdge', node?: { __typename?: 'Task', id: string, status: string, running?: boolean | null, error?: string | null } | null } | null> } | null, images?: { __typename?: 'ImageConnection', edges: Array<{ __typename?: 'ImageEdge', node?: { __typename?: 'Image', id: string, filename?: string | null } | null } | null> } | null } | null } | null> } | null };

export type AllTasksQueryVariables = Exact<{
  sort?: InputMaybe<Array<InputMaybe<TaskSortEnum>> | InputMaybe<TaskSortEnum>>;
}>;


export type AllTasksQuery = { __typename?: 'Query', allTasks?: { __typename?: 'TaskConnection', edges: Array<{ __typename?: 'TaskEdge', node?: { __typename?: 'Task', id: string, running?: boolean | null, status: string, error?: string | null, priority?: number | null, workerId: string, kind: string, createdOn?: any | null, updatedOn?: any | null, requestId?: number | null, images?: { __typename?: 'ImageConnection', edges: Array<{ __typename?: 'ImageEdge', node?: { __typename?: 'Image', id: string, filename?: string | null } | null } | null> } | null } | null } | null> } | null };

export type AllImagesQueryVariables = Exact<{
  sort?: InputMaybe<Array<InputMaybe<ImageSortEnum>> | InputMaybe<ImageSortEnum>>;
}>;


export type AllImagesQuery = { __typename?: 'Query', allImages?: { __typename?: 'ImageConnection', edges: Array<{ __typename?: 'ImageEdge', node?: { __typename?: 'Image', id: string, filename?: string | null, selected?: boolean | null, createdOn?: any | null, updatedOn?: any | null, requestId?: number | null, taskId?: number | null } | null } | null> } | null };


export const AllRequestsDocument = gql`
    query AllRequests($sort: [RequestSortEnum]) {
  allRequests(sort: $sort) {
    edges {
      node {
        id
        prompt
        priority
        approved
        generated
        kind
        createdOn
        updatedOn
        tasks {
          edges {
            node {
              id
              status
              running
              error
            }
          }
        }
        images {
          edges {
            node {
              id
              filename
            }
          }
        }
      }
    }
  }
}
    `;

export function useAllRequestsQuery(options?: Omit<Urql.UseQueryArgs<AllRequestsQueryVariables>, 'query'>) {
  return Urql.useQuery<AllRequestsQuery, AllRequestsQueryVariables>({ query: AllRequestsDocument, ...options });
};
export const AllTasksDocument = gql`
    query AllTasks($sort: [TaskSortEnum]) {
  allTasks(sort: $sort) {
    edges {
      node {
        id
        running
        status
        error
        priority
        workerId
        kind
        createdOn
        updatedOn
        requestId
        images {
          edges {
            node {
              id
              filename
            }
          }
        }
      }
    }
  }
}
    `;

export function useAllTasksQuery(options?: Omit<Urql.UseQueryArgs<AllTasksQueryVariables>, 'query'>) {
  return Urql.useQuery<AllTasksQuery, AllTasksQueryVariables>({ query: AllTasksDocument, ...options });
};
export const AllImagesDocument = gql`
    query AllImages($sort: [ImageSortEnum]) {
  allImages(sort: $sort) {
    edges {
      node {
        id
        filename
        selected
        createdOn
        updatedOn
        requestId
        taskId
      }
    }
  }
}
    `;

export function useAllImagesQuery(options?: Omit<Urql.UseQueryArgs<AllImagesQueryVariables>, 'query'>) {
  return Urql.useQuery<AllImagesQuery, AllImagesQueryVariables>({ query: AllImagesDocument, ...options });
};