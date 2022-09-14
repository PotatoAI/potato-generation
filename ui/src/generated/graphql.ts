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
  JSONString: any;
};

export type CreateRequest = {
  __typename?: 'CreateRequest';
  ok?: Maybe<Scalars['Boolean']>;
  request?: Maybe<Request>;
};

export type DoAction = {
  __typename?: 'DoAction';
  ok?: Maybe<Scalars['Boolean']>;
};

export type Image = Node & {
  __typename?: 'Image';
  createdOn?: Maybe<Scalars['DateTime']>;
  filename?: Maybe<Scalars['String']>;
  hqoid?: Maybe<Scalars['JSONString']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  oid?: Maybe<Scalars['JSONString']>;
  request?: Maybe<Request>;
  requestId?: Maybe<Scalars['Int']>;
  selected?: Maybe<Scalars['Boolean']>;
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
  HqoidAsc = 'HQOID_ASC',
  HqoidDesc = 'HQOID_DESC',
  IdAsc = 'ID_ASC',
  IdDesc = 'ID_DESC',
  OidAsc = 'OID_ASC',
  OidDesc = 'OID_DESC',
  RequestIdAsc = 'REQUEST_ID_ASC',
  RequestIdDesc = 'REQUEST_ID_DESC',
  SelectedAsc = 'SELECTED_ASC',
  SelectedDesc = 'SELECTED_DESC',
  UpdatedOnAsc = 'UPDATED_ON_ASC',
  UpdatedOnDesc = 'UPDATED_ON_DESC'
}

export type LargeObject = {
  __typename?: 'LargeObject';
  data: Scalars['String'];
  oid: Scalars['Int'];
};

export type Mutation = {
  __typename?: 'Mutation';
  createRequest?: Maybe<CreateRequest>;
  doAction?: Maybe<DoAction>;
};


export type MutationCreateRequestArgs = {
  count?: InputMaybe<Scalars['Int']>;
  prompt?: InputMaybe<Scalars['String']>;
};


export type MutationDoActionArgs = {
  action: Scalars['String'];
  ids?: InputMaybe<Array<Scalars['String']>>;
  metadata?: InputMaybe<Array<Scalars['String']>>;
  model: Scalars['String'];
};

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
  allVideos?: Maybe<VideoConnection>;
  imagesById?: Maybe<Array<Maybe<Image>>>;
  inputFiles?: Maybe<Array<Maybe<Scalars['String']>>>;
  largeObjects?: Maybe<Array<Maybe<LargeObject>>>;
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


export type QueryAllVideosArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  sort?: InputMaybe<Array<InputMaybe<VideoSortEnum>>>;
};


export type QueryImagesByIdArgs = {
  imageIds?: InputMaybe<Array<Scalars['String']>>;
};


export type QueryLargeObjectsArgs = {
  oids?: InputMaybe<Array<Scalars['Int']>>;
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
  updatedOn?: Maybe<Scalars['DateTime']>;
  videos?: Maybe<VideoConnection>;
};


export type RequestImagesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
};


export type RequestVideosArgs = {
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

export type Video = Node & {
  __typename?: 'Video';
  createdOn?: Maybe<Scalars['DateTime']>;
  filename?: Maybe<Scalars['String']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  oid?: Maybe<Scalars['JSONString']>;
  request?: Maybe<Request>;
  requestId?: Maybe<Scalars['Int']>;
  selected?: Maybe<Scalars['Boolean']>;
  updatedOn?: Maybe<Scalars['DateTime']>;
};

export type VideoConnection = {
  __typename?: 'VideoConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<VideoEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
};

/** A Relay edge containing a `Video` and its cursor. */
export type VideoEdge = {
  __typename?: 'VideoEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<Video>;
};

/** An enumeration. */
export enum VideoSortEnum {
  CreatedOnAsc = 'CREATED_ON_ASC',
  CreatedOnDesc = 'CREATED_ON_DESC',
  FilenameAsc = 'FILENAME_ASC',
  FilenameDesc = 'FILENAME_DESC',
  IdAsc = 'ID_ASC',
  IdDesc = 'ID_DESC',
  OidAsc = 'OID_ASC',
  OidDesc = 'OID_DESC',
  RequestIdAsc = 'REQUEST_ID_ASC',
  RequestIdDesc = 'REQUEST_ID_DESC',
  SelectedAsc = 'SELECTED_ASC',
  SelectedDesc = 'SELECTED_DESC',
  UpdatedOnAsc = 'UPDATED_ON_ASC',
  UpdatedOnDesc = 'UPDATED_ON_DESC'
}

export type AllRequestsQueryVariables = Exact<{
  sort?: InputMaybe<Array<InputMaybe<RequestSortEnum>> | InputMaybe<RequestSortEnum>>;
}>;


export type AllRequestsQuery = { __typename?: 'Query', allRequests?: { __typename?: 'RequestConnection', edges: Array<{ __typename?: 'RequestEdge', node?: { __typename?: 'Request', id: string, prompt: string, priority?: number | null, approved?: boolean | null, generated?: boolean | null, kind: string, createdOn?: any | null, updatedOn?: any | null, images?: { __typename?: 'ImageConnection', edges: Array<{ __typename?: 'ImageEdge', node?: { __typename?: 'Image', id: string, filename?: string | null, oid?: any | null } | null } | null> } | null, videos?: { __typename?: 'VideoConnection', edges: Array<{ __typename?: 'VideoEdge', node?: { __typename?: 'Video', id: string, filename?: string | null, oid?: any | null } | null } | null> } | null } | null } | null> } | null };

export type AllImagesQueryVariables = Exact<{
  sort?: InputMaybe<Array<InputMaybe<ImageSortEnum>> | InputMaybe<ImageSortEnum>>;
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;


export type AllImagesQuery = { __typename?: 'Query', allImages?: { __typename?: 'ImageConnection', edges: Array<{ __typename?: 'ImageEdge', node?: { __typename?: 'Image', id: string, filename?: string | null, selected?: boolean | null, createdOn?: any | null, updatedOn?: any | null, requestId?: number | null, oid?: any | null } | null } | null> } | null };

export type AllVideosQueryVariables = Exact<{
  sort?: InputMaybe<Array<InputMaybe<VideoSortEnum>> | InputMaybe<VideoSortEnum>>;
}>;


export type AllVideosQuery = { __typename?: 'Query', allVideos?: { __typename?: 'VideoConnection', edges: Array<{ __typename?: 'VideoEdge', node?: { __typename?: 'Video', id: string, filename?: string | null, selected?: boolean | null, createdOn?: any | null, updatedOn?: any | null, requestId?: number | null, oid?: any | null } | null } | null> } | null };

export type LargeObjectsQueryVariables = Exact<{
  oids?: InputMaybe<Array<Scalars['Int']> | Scalars['Int']>;
}>;


export type LargeObjectsQuery = { __typename?: 'Query', largeObjects?: Array<{ __typename?: 'LargeObject', oid: number, data: string } | null> | null };

export type CreateRequestMutationVariables = Exact<{
  prompt?: InputMaybe<Scalars['String']>;
  count?: InputMaybe<Scalars['Int']>;
}>;


export type CreateRequestMutation = { __typename?: 'Mutation', createRequest?: { __typename?: 'CreateRequest', ok?: boolean | null, request?: { __typename?: 'Request', id: string } | null } | null };

export type DoActionMutationVariables = Exact<{
  ids?: InputMaybe<Array<Scalars['String']> | Scalars['String']>;
  action: Scalars['String'];
  model: Scalars['String'];
  metadata?: InputMaybe<Array<Scalars['String']> | Scalars['String']>;
}>;


export type DoActionMutation = { __typename?: 'Mutation', doAction?: { __typename?: 'DoAction', ok?: boolean | null } | null };

export type InputFilesQueryVariables = Exact<{ [key: string]: never; }>;


export type InputFilesQuery = { __typename?: 'Query', inputFiles?: Array<string | null> | null };

export type ImagesByIdQueryVariables = Exact<{
  imageIds?: InputMaybe<Array<Scalars['String']> | Scalars['String']>;
}>;


export type ImagesByIdQuery = { __typename?: 'Query', imagesById?: Array<{ __typename?: 'Image', id: string, filename?: string | null, selected?: boolean | null, createdOn?: any | null, updatedOn?: any | null, requestId?: number | null, oid?: any | null, hqoid?: any | null } | null> | null };


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
        images {
          edges {
            node {
              id
              filename
              oid
            }
          }
        }
        videos {
          edges {
            node {
              id
              filename
              oid
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
export const AllImagesDocument = gql`
    query AllImages($sort: [ImageSortEnum], $first: Int, $after: String) {
  allImages(sort: $sort, first: $first, after: $after) {
    edges {
      node {
        id
        filename
        selected
        createdOn
        updatedOn
        requestId
        oid
      }
    }
  }
}
    `;

export function useAllImagesQuery(options?: Omit<Urql.UseQueryArgs<AllImagesQueryVariables>, 'query'>) {
  return Urql.useQuery<AllImagesQuery, AllImagesQueryVariables>({ query: AllImagesDocument, ...options });
};
export const AllVideosDocument = gql`
    query AllVideos($sort: [VideoSortEnum]) {
  allVideos(sort: $sort) {
    edges {
      node {
        id
        filename
        selected
        createdOn
        updatedOn
        requestId
        oid
      }
    }
  }
}
    `;

export function useAllVideosQuery(options?: Omit<Urql.UseQueryArgs<AllVideosQueryVariables>, 'query'>) {
  return Urql.useQuery<AllVideosQuery, AllVideosQueryVariables>({ query: AllVideosDocument, ...options });
};
export const LargeObjectsDocument = gql`
    query LargeObjects($oids: [Int!]) {
  largeObjects(oids: $oids) {
    oid
    data
  }
}
    `;

export function useLargeObjectsQuery(options?: Omit<Urql.UseQueryArgs<LargeObjectsQueryVariables>, 'query'>) {
  return Urql.useQuery<LargeObjectsQuery, LargeObjectsQueryVariables>({ query: LargeObjectsDocument, ...options });
};
export const CreateRequestDocument = gql`
    mutation CreateRequest($prompt: String, $count: Int) {
  createRequest(prompt: $prompt, count: $count) {
    ok
    request {
      id
    }
  }
}
    `;

export function useCreateRequestMutation() {
  return Urql.useMutation<CreateRequestMutation, CreateRequestMutationVariables>(CreateRequestDocument);
};
export const DoActionDocument = gql`
    mutation DoAction($ids: [String!], $action: String!, $model: String!, $metadata: [String!]) {
  doAction(ids: $ids, action: $action, model: $model, metadata: $metadata) {
    ok
  }
}
    `;

export function useDoActionMutation() {
  return Urql.useMutation<DoActionMutation, DoActionMutationVariables>(DoActionDocument);
};
export const InputFilesDocument = gql`
    query InputFiles {
  inputFiles
}
    `;

export function useInputFilesQuery(options?: Omit<Urql.UseQueryArgs<InputFilesQueryVariables>, 'query'>) {
  return Urql.useQuery<InputFilesQuery, InputFilesQueryVariables>({ query: InputFilesDocument, ...options });
};
export const ImagesByIdDocument = gql`
    query ImagesById($imageIds: [String!]) {
  imagesById(imageIds: $imageIds) {
    id
    filename
    selected
    createdOn
    updatedOn
    requestId
    oid
    hqoid
  }
}
    `;

export function useImagesByIdQuery(options?: Omit<Urql.UseQueryArgs<ImagesByIdQueryVariables>, 'query'>) {
  return Urql.useQuery<ImagesByIdQuery, ImagesByIdQueryVariables>({ query: ImagesByIdDocument, ...options });
};