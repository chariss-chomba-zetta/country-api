--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3 (Debian 13.3-1.pgdg100+1)
-- Dumped by pg_dump version 13.3 (Debian 13.3-1.pgdg100+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: menus_dfsservice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_dfsservice (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(36) NOT NULL,
    service_function character varying(255) NOT NULL,
    url character varying(255) NOT NULL,
    method character varying(10) NOT NULL,
    session_key character varying(255),
    service_degradation_key "char"
);


ALTER TABLE public.menus_dfsservice OWNER TO postgres;

--
-- Name: menus_dfsservice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_dfsservice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_dfsservice_id_seq OWNER TO postgres;

--
-- Name: menus_dfsservice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_dfsservice_id_seq OWNED BY public.menus_dfsservice.id;


--
-- Name: menus_errorlabel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_errorlabel (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    error_message character varying(150) NOT NULL,
    language_id bigint NOT NULL
);


ALTER TABLE public.menus_errorlabel OWNER TO postgres;

--
-- Name: menus_errorlabel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_errorlabel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_errorlabel_id_seq OWNER TO postgres;

--
-- Name: menus_errorlabel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_errorlabel_id_seq OWNED BY public.menus_errorlabel.id;


--
-- Name: menus_language; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_language (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    language_code character varying(2) NOT NULL,
    language_name character varying(50) NOT NULL
);


ALTER TABLE public.menus_language OWNER TO postgres;

--
-- Name: menus_language_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_language_id_seq OWNER TO postgres;

--
-- Name: menus_language_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_language_id_seq OWNED BY public.menus_language.id;


--
-- Name: menus_menuitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_menuitem (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    item_text character varying(512) NOT NULL,
    item_value character varying(512) NOT NULL,
    with_items character varying(512) NOT NULL,
    session_key character varying(512) NOT NULL,
    ussd_menu_id bigint NOT NULL
);


ALTER TABLE public.menus_menuitem OWNER TO postgres;

--
-- Name: menus_menuitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_menuitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_menuitem_id_seq OWNER TO postgres;

--
-- Name: menus_menuitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_menuitem_id_seq OWNED BY public.menus_menuitem.id;


--
-- Name: menus_menuoption; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_menuoption (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    option_text character varying(255) NOT NULL,
    "order" smallint NOT NULL,
    language_id bigint NOT NULL,
    menu_id bigint NOT NULL,
    next_screen_id bigint NOT NULL,
    CONSTRAINT menus_menuoption_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.menus_menuoption OWNER TO postgres;

--
-- Name: menus_menuoption_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_menuoption_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_menuoption_id_seq OWNER TO postgres;

--
-- Name: menus_menuoption_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_menuoption_id_seq OWNED BY public.menus_menuoption.id;


--
-- Name: menus_menutype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_menutype (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.menus_menutype OWNER TO postgres;

--
-- Name: menus_menutype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_menutype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_menutype_id_seq OWNER TO postgres;

--
-- Name: menus_menutype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_menutype_id_seq OWNED BY public.menus_menutype.id;


--
-- Name: menus_navigationlabel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_navigationlabel (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    back_label character varying(25) NOT NULL,
    main_menu_label character varying(25) NOT NULL,
    pin_reset_label character varying(25) NOT NULL,
    language_id bigint NOT NULL
);


ALTER TABLE public.menus_navigationlabel OWNER TO postgres;

--
-- Name: menus_navigationlabel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_navigationlabel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_navigationlabel_id_seq OWNER TO postgres;

--
-- Name: menus_navigationlabel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_navigationlabel_id_seq OWNED BY public.menus_navigationlabel.id;


--
-- Name: menus_routeroption; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_routeroption (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    menu_expression character varying(1024) NOT NULL,
    menu_id bigint NOT NULL,
    next_screen_id bigint NOT NULL
);


ALTER TABLE public.menus_routeroption OWNER TO postgres;

--
-- Name: menus_routeroption_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_routeroption_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_routeroption_id_seq OWNER TO postgres;

--
-- Name: menus_routeroption_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_routeroption_id_seq OWNED BY public.menus_routeroption.id;


--
-- Name: menus_shortcode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_shortcode (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    institution character varying(255) NOT NULL,
    shortcode character varying(50) NOT NULL,
    country character varying(2) NOT NULL
);


ALTER TABLE public.menus_shortcode OWNER TO postgres;

--
-- Name: menus_shortcode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_shortcode_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_shortcode_id_seq OWNER TO postgres;

--
-- Name: menus_shortcode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_shortcode_id_seq OWNED BY public.menus_shortcode.id;


--
-- Name: menus_ussdlabel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_ussdlabel (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    label_text character varying(255),
    language_id bigint NOT NULL,
    menu_id bigint NOT NULL
);


ALTER TABLE public.menus_ussdlabel OWNER TO postgres;

--
-- Name: menus_ussdlabel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_ussdlabel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_ussdlabel_id_seq OWNER TO postgres;

--
-- Name: menus_ussdlabel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_ussdlabel_id_seq OWNED BY public.menus_ussdlabel.id;


--
-- Name: menus_ussdmenu; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus_ussdmenu (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    name character varying(50) NOT NULL,
    has_options boolean NOT NULL,
    input_identifier character varying(50) NOT NULL,
    input_screen_has_back boolean NOT NULL,
    input_screen_has_home boolean NOT NULL,
    input_screen_has_pin_reset boolean NOT NULL,
    menu_screen_has_back boolean NOT NULL,
    menu_screen_has_home boolean NOT NULL,
    input_screen_back_screen_id bigint,
    menu_screen_back_screen_id bigint,
    menu_type_id bigint NOT NULL,
    next_screen_id bigint,
    dfs_service_id bigint,
    shortcode_id bigint NOT NULL
);


ALTER TABLE public.menus_ussdmenu OWNER TO postgres;

--
-- Name: menus_ussdmenu_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_ussdmenu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_ussdmenu_id_seq OWNER TO postgres;

--
-- Name: menus_ussdmenu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_ussdmenu_id_seq OWNED BY public.menus_ussdmenu.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: menus_dfsservice id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_dfsservice ALTER COLUMN id SET DEFAULT nextval('public.menus_dfsservice_id_seq'::regclass);


--
-- Name: menus_errorlabel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_errorlabel ALTER COLUMN id SET DEFAULT nextval('public.menus_errorlabel_id_seq'::regclass);


--
-- Name: menus_language id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_language ALTER COLUMN id SET DEFAULT nextval('public.menus_language_id_seq'::regclass);


--
-- Name: menus_menuitem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuitem ALTER COLUMN id SET DEFAULT nextval('public.menus_menuitem_id_seq'::regclass);


--
-- Name: menus_menuoption id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuoption ALTER COLUMN id SET DEFAULT nextval('public.menus_menuoption_id_seq'::regclass);


--
-- Name: menus_menutype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menutype ALTER COLUMN id SET DEFAULT nextval('public.menus_menutype_id_seq'::regclass);


--
-- Name: menus_navigationlabel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_navigationlabel ALTER COLUMN id SET DEFAULT nextval('public.menus_navigationlabel_id_seq'::regclass);


--
-- Name: menus_routeroption id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_routeroption ALTER COLUMN id SET DEFAULT nextval('public.menus_routeroption_id_seq'::regclass);


--
-- Name: menus_shortcode id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_shortcode ALTER COLUMN id SET DEFAULT nextval('public.menus_shortcode_id_seq'::regclass);


--
-- Name: menus_ussdlabel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdlabel ALTER COLUMN id SET DEFAULT nextval('public.menus_ussdlabel_id_seq'::regclass);


--
-- Name: menus_ussdmenu id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu ALTER COLUMN id SET DEFAULT nextval('public.menus_ussdmenu_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add ussd menu	7	add_ussdmenu
26	Can change ussd menu	7	change_ussdmenu
27	Can delete ussd menu	7	delete_ussdmenu
28	Can view ussd menu	7	view_ussdmenu
29	Can add language	8	add_language
30	Can change language	8	change_language
31	Can delete language	8	delete_language
32	Can view language	8	view_language
33	Can add menu type	9	add_menutype
34	Can change menu type	9	change_menutype
35	Can delete menu type	9	delete_menutype
36	Can view menu type	9	view_menutype
37	Can add ussd label	10	add_ussdlabel
38	Can change ussd label	10	change_ussdlabel
39	Can delete ussd label	10	delete_ussdlabel
40	Can view ussd label	10	view_ussdlabel
41	Can add dfs service	11	add_dfsservice
42	Can change dfs service	11	change_dfsservice
43	Can delete dfs service	11	delete_dfsservice
44	Can view dfs service	11	view_dfsservice
45	Can add short code	12	add_shortcode
46	Can change short code	12	change_shortcode
47	Can delete short code	12	delete_shortcode
48	Can view short code	12	view_shortcode
49	Can add navigation label	13	add_navigationlabel
50	Can change navigation label	13	change_navigationlabel
51	Can delete navigation label	13	delete_navigationlabel
52	Can view navigation label	13	view_navigationlabel
53	Can add menu option	14	add_menuoption
54	Can change menu option	14	change_menuoption
55	Can delete menu option	14	delete_menuoption
56	Can view menu option	14	view_menuoption
57	Can add menu item	15	add_menuitem
58	Can change menu item	15	change_menuitem
59	Can delete menu item	15	delete_menuitem
60	Can view menu item	15	view_menuitem
61	Can add router option	16	add_routeroption
62	Can change router option	16	change_routeroption
63	Can delete router option	16	delete_routeroption
64	Can view router option	16	view_routeroption
65	Can add error label	17	add_errorlabel
66	Can change error label	17	change_errorlabel
67	Can delete error label	17	delete_errorlabel
68	Can view error label	17	view_errorlabel
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$260000$hGCMvGAJRGMEJnyD1xQ0sa$a77kvsdWLT3fAvTRnYy/3Q/pbrwulQ786ATwhyv7JIY=	2024-02-27 12:35:54.518752+00	t	chariss			charisschomba@gmail.com	t	t	2024-02-27 12:35:37.611306+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2024-02-27 13:29:30.067154+00	1	English	1	[{"added": {}}]	8	2
2	2024-02-27 13:29:40.439072+00	2	Swahili	1	[{"added": {}}]	8	2
3	2024-02-27 13:29:51.423696+00	2	Swahili	2	[{"changed": {"fields": ["Is active"]}}]	8	2
4	2024-02-27 13:30:37.213177+00	1	347	1	[{"added": {}}]	12	2
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	menus	ussdmenu
8	menus	language
9	menus	menutype
10	menus	ussdlabel
11	menus	dfsservice
12	menus	shortcode
13	menus	navigationlabel
14	menus	menuoption
15	menus	menuitem
16	menus	routeroption
17	menus	errorlabel
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2024-02-27 09:49:01.187051+00
2	auth	0001_initial	2024-02-27 09:49:01.397916+00
3	admin	0001_initial	2024-02-27 09:49:01.487224+00
4	admin	0002_logentry_remove_auto_add	2024-02-27 09:49:01.507314+00
5	admin	0003_logentry_add_action_flag_choices	2024-02-27 09:49:01.535557+00
6	contenttypes	0002_remove_content_type_name	2024-02-27 09:49:01.6091+00
7	auth	0002_alter_permission_name_max_length	2024-02-27 09:49:01.649271+00
8	auth	0003_alter_user_email_max_length	2024-02-27 09:49:01.688636+00
9	auth	0004_alter_user_username_opts	2024-02-27 09:49:01.720516+00
10	auth	0005_alter_user_last_login_null	2024-02-27 09:49:01.753424+00
11	auth	0006_require_contenttypes_0002	2024-02-27 09:49:01.76647+00
12	auth	0007_alter_validators_add_error_messages	2024-02-27 09:49:01.799758+00
13	auth	0008_alter_user_username_max_length	2024-02-27 09:49:01.841473+00
14	auth	0009_alter_user_last_name_max_length	2024-02-27 09:49:01.870214+00
15	auth	0010_alter_group_name_max_length	2024-02-27 09:49:01.896706+00
16	auth	0011_update_proxy_permissions	2024-02-27 09:49:01.929226+00
17	auth	0012_alter_user_first_name_max_length	2024-02-27 09:49:01.96966+00
18	sessions	0001_initial	2024-02-27 09:49:02.043511+00
19	menus	0001_initial	2024-02-27 12:32:28.907469+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
eys8qki35nb216355wnh4o3s9fyaao3s	.eJxVjMEOwiAQRP-FsyGU0qV49N5vIMuySNVAUtqT8d9tkx50jvPezFt43Nbst8aLn6O4Ci0uv11AenI5QHxguVdJtazLHOShyJM2OdXIr9vp_h1kbHlfU-ysoj3IViW0pCC50emknOsHhaNNZIAN2R4sd8ZFcABgYuABtCLx-QL58Tfs:1rewgc:ND0XnEPUP8Cw39MBphh9gDEN8kxnkatx1J0sjFaA3Wc	2024-03-12 12:35:54.52379+00
\.


--
-- Data for Name: menus_dfsservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_dfsservice (id, created_at, updated_at, name, service_function, url, method, session_key, service_degradation_key) FROM stdin;
\.


--
-- Data for Name: menus_errorlabel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_errorlabel (id, created_at, updated_at, error_message, language_id) FROM stdin;
\.


--
-- Data for Name: menus_language; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_language (id, created_at, updated_at, is_active, language_code, language_name) FROM stdin;
1	2024-02-27 13:29:30.055634+00	2024-02-27 13:29:30.055671+00	t	en	English
2	2024-02-27 13:29:40.427724+00	2024-02-27 13:29:51.418832+00	t	sw	Swahili
\.


--
-- Data for Name: menus_menuitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_menuitem (id, created_at, updated_at, item_text, item_value, with_items, session_key, ussd_menu_id) FROM stdin;
\.


--
-- Data for Name: menus_menuoption; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_menuoption (id, created_at, updated_at, is_active, option_text, "order", language_id, menu_id, next_screen_id) FROM stdin;
\.


--
-- Data for Name: menus_menutype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_menutype (id, created_at, updated_at, name) FROM stdin;
1	2021-04-26 09:09:22.483+00	2021-04-26 09:09:22.483+00	initial_screen
2	2021-04-26 09:09:30.483+00	2021-04-26 09:09:30.483+00	menu_screen
3	2021-04-26 09:09:38.633+00	2021-04-26 09:09:38.633+00	input_screen
4	2021-04-26 09:09:48.397+00	2021-04-26 09:09:48.397+00	function_screen
5	2021-04-26 09:09:56.173+00	2021-04-26 09:09:56.173+00	quit_screen
6	2021-04-26 09:10:06.41+00	2021-04-26 09:10:06.41+00	router_screen
7	2021-04-26 09:40:33.887+00	2021-04-26 09:40:33.887+00	quit_screen
\.


--
-- Data for Name: menus_navigationlabel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_navigationlabel (id, created_at, updated_at, back_label, main_menu_label, pin_reset_label, language_id) FROM stdin;
\.


--
-- Data for Name: menus_routeroption; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_routeroption (id, created_at, updated_at, is_active, menu_expression, menu_id, next_screen_id) FROM stdin;
\.


--
-- Data for Name: menus_shortcode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_shortcode (id, created_at, updated_at, is_active, institution, shortcode, country) FROM stdin;
1	2024-02-27 13:30:37.208838+00	2024-02-27 13:30:37.20895+00	t	Equity Group Foundation	347	KE
\.


--
-- Data for Name: menus_ussdlabel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_ussdlabel (id, created_at, updated_at, label_text, language_id, menu_id) FROM stdin;
\.


--
-- Data for Name: menus_ussdmenu; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus_ussdmenu (id, created_at, updated_at, is_active, name, has_options, input_identifier, input_screen_has_back, input_screen_has_home, input_screen_has_pin_reset, menu_screen_has_back, menu_screen_has_home, input_screen_back_screen_id, menu_screen_back_screen_id, menu_type_id, next_screen_id, dfs_service_id, shortcode_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 68, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 2, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 4, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 17, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 19, true);


--
-- Name: menus_dfsservice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_dfsservice_id_seq', 1, false);


--
-- Name: menus_errorlabel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_errorlabel_id_seq', 1, false);


--
-- Name: menus_language_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_language_id_seq', 2, true);


--
-- Name: menus_menuitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_menuitem_id_seq', 1, false);


--
-- Name: menus_menuoption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_menuoption_id_seq', 1, false);


--
-- Name: menus_menutype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_menutype_id_seq', 1, false);


--
-- Name: menus_navigationlabel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_navigationlabel_id_seq', 1, false);


--
-- Name: menus_routeroption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_routeroption_id_seq', 1, false);


--
-- Name: menus_shortcode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_shortcode_id_seq', 1, true);


--
-- Name: menus_ussdlabel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_ussdlabel_id_seq', 1, false);


--
-- Name: menus_ussdmenu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_ussdmenu_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: menus_dfsservice menus_dfsservice_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_dfsservice
    ADD CONSTRAINT menus_dfsservice_name_key UNIQUE (name);


--
-- Name: menus_dfsservice menus_dfsservice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_dfsservice
    ADD CONSTRAINT menus_dfsservice_pkey PRIMARY KEY (id);


--
-- Name: menus_dfsservice menus_dfsservice_service_function_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_dfsservice
    ADD CONSTRAINT menus_dfsservice_service_function_key UNIQUE (service_function);


--
-- Name: menus_errorlabel menus_errorlabel_language_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_errorlabel
    ADD CONSTRAINT menus_errorlabel_language_id_key UNIQUE (language_id);


--
-- Name: menus_errorlabel menus_errorlabel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_errorlabel
    ADD CONSTRAINT menus_errorlabel_pkey PRIMARY KEY (id);


--
-- Name: menus_language menus_language_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_language
    ADD CONSTRAINT menus_language_pkey PRIMARY KEY (id);


--
-- Name: menus_menuitem menus_menuitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuitem
    ADD CONSTRAINT menus_menuitem_pkey PRIMARY KEY (id);


--
-- Name: menus_menuoption menus_menuoption_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuoption
    ADD CONSTRAINT menus_menuoption_pkey PRIMARY KEY (id);


--
-- Name: menus_menutype menus_menutype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menutype
    ADD CONSTRAINT menus_menutype_pkey PRIMARY KEY (id);


--
-- Name: menus_navigationlabel menus_navigationlabel_language_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_navigationlabel
    ADD CONSTRAINT menus_navigationlabel_language_id_key UNIQUE (language_id);


--
-- Name: menus_navigationlabel menus_navigationlabel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_navigationlabel
    ADD CONSTRAINT menus_navigationlabel_pkey PRIMARY KEY (id);


--
-- Name: menus_routeroption menus_routeroption_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_routeroption
    ADD CONSTRAINT menus_routeroption_pkey PRIMARY KEY (id);


--
-- Name: menus_shortcode menus_shortcode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_shortcode
    ADD CONSTRAINT menus_shortcode_pkey PRIMARY KEY (id);


--
-- Name: menus_ussdlabel menus_ussdlabel_menu_id_language_id_6f4c1fec_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdlabel
    ADD CONSTRAINT menus_ussdlabel_menu_id_language_id_6f4c1fec_uniq UNIQUE (menu_id, language_id);


--
-- Name: menus_ussdlabel menus_ussdlabel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdlabel
    ADD CONSTRAINT menus_ussdlabel_pkey PRIMARY KEY (id);


--
-- Name: menus_ussdmenu menus_ussdmenu_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_name_key UNIQUE (name);


--
-- Name: menus_ussdmenu menus_ussdmenu_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: menus_dfsservice_name_8fc7b6cf_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_dfsservice_name_8fc7b6cf_like ON public.menus_dfsservice USING btree (name varchar_pattern_ops);


--
-- Name: menus_dfsservice_service_function_fe99c49b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_dfsservice_service_function_fe99c49b_like ON public.menus_dfsservice USING btree (service_function varchar_pattern_ops);


--
-- Name: menus_menuitem_ussd_menu_id_04e0dd32; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_menuitem_ussd_menu_id_04e0dd32 ON public.menus_menuitem USING btree (ussd_menu_id);


--
-- Name: menus_menuoption_language_id_81353af4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_menuoption_language_id_81353af4 ON public.menus_menuoption USING btree (language_id);


--
-- Name: menus_menuoption_menu_id_7241c601; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_menuoption_menu_id_7241c601 ON public.menus_menuoption USING btree (menu_id);


--
-- Name: menus_menuoption_next_screen_id_a83bb426; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_menuoption_next_screen_id_a83bb426 ON public.menus_menuoption USING btree (next_screen_id);


--
-- Name: menus_routeroption_menu_id_1999c00d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_routeroption_menu_id_1999c00d ON public.menus_routeroption USING btree (menu_id);


--
-- Name: menus_routeroption_next_screen_id_f370d42a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_routeroption_next_screen_id_f370d42a ON public.menus_routeroption USING btree (next_screen_id);


--
-- Name: menus_ussdlabel_language_id_9e14e252; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdlabel_language_id_9e14e252 ON public.menus_ussdlabel USING btree (language_id);


--
-- Name: menus_ussdlabel_menu_id_7689193d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdlabel_menu_id_7689193d ON public.menus_ussdlabel USING btree (menu_id);


--
-- Name: menus_ussdmenu_dfs_service_id_2438e833; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdmenu_dfs_service_id_2438e833 ON public.menus_ussdmenu USING btree (dfs_service_id);


--
-- Name: menus_ussdmenu_input_screen_back_screen_id_74e6ebc5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdmenu_input_screen_back_screen_id_74e6ebc5 ON public.menus_ussdmenu USING btree (input_screen_back_screen_id);


--
-- Name: menus_ussdmenu_menu_screen_back_screen_id_f2d39a43; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdmenu_menu_screen_back_screen_id_f2d39a43 ON public.menus_ussdmenu USING btree (menu_screen_back_screen_id);


--
-- Name: menus_ussdmenu_menu_type_id_d082a804; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdmenu_menu_type_id_d082a804 ON public.menus_ussdmenu USING btree (menu_type_id);


--
-- Name: menus_ussdmenu_name_1374af44_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdmenu_name_1374af44_like ON public.menus_ussdmenu USING btree (name varchar_pattern_ops);


--
-- Name: menus_ussdmenu_next_screen_id_a244cc38; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdmenu_next_screen_id_a244cc38 ON public.menus_ussdmenu USING btree (next_screen_id);


--
-- Name: menus_ussdmenu_shortcode_id_625c15cf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX menus_ussdmenu_shortcode_id_625c15cf ON public.menus_ussdmenu USING btree (shortcode_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_errorlabel menus_errorlabel_language_id_a25e366d_fk_menus_language_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_errorlabel
    ADD CONSTRAINT menus_errorlabel_language_id_a25e366d_fk_menus_language_id FOREIGN KEY (language_id) REFERENCES public.menus_language(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_menuitem menus_menuitem_ussd_menu_id_04e0dd32_fk_menus_ussdmenu_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuitem
    ADD CONSTRAINT menus_menuitem_ussd_menu_id_04e0dd32_fk_menus_ussdmenu_id FOREIGN KEY (ussd_menu_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_menuoption menus_menuoption_language_id_81353af4_fk_menus_language_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuoption
    ADD CONSTRAINT menus_menuoption_language_id_81353af4_fk_menus_language_id FOREIGN KEY (language_id) REFERENCES public.menus_language(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_menuoption menus_menuoption_menu_id_7241c601_fk_menus_ussdmenu_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuoption
    ADD CONSTRAINT menus_menuoption_menu_id_7241c601_fk_menus_ussdmenu_id FOREIGN KEY (menu_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_menuoption menus_menuoption_next_screen_id_a83bb426_fk_menus_ussdmenu_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_menuoption
    ADD CONSTRAINT menus_menuoption_next_screen_id_a83bb426_fk_menus_ussdmenu_id FOREIGN KEY (next_screen_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_navigationlabel menus_navigationlabel_language_id_b951248b_fk_menus_language_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_navigationlabel
    ADD CONSTRAINT menus_navigationlabel_language_id_b951248b_fk_menus_language_id FOREIGN KEY (language_id) REFERENCES public.menus_language(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_routeroption menus_routeroption_menu_id_1999c00d_fk_menus_ussdmenu_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_routeroption
    ADD CONSTRAINT menus_routeroption_menu_id_1999c00d_fk_menus_ussdmenu_id FOREIGN KEY (menu_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_routeroption menus_routeroption_next_screen_id_f370d42a_fk_menus_ussdmenu_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_routeroption
    ADD CONSTRAINT menus_routeroption_next_screen_id_f370d42a_fk_menus_ussdmenu_id FOREIGN KEY (next_screen_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdlabel menus_ussdlabel_language_id_9e14e252_fk_menus_language_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdlabel
    ADD CONSTRAINT menus_ussdlabel_language_id_9e14e252_fk_menus_language_id FOREIGN KEY (language_id) REFERENCES public.menus_language(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdlabel menus_ussdlabel_menu_id_7689193d_fk_menus_ussdmenu_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdlabel
    ADD CONSTRAINT menus_ussdlabel_menu_id_7689193d_fk_menus_ussdmenu_id FOREIGN KEY (menu_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdmenu menus_ussdmenu_dfs_service_id_2438e833_fk_menus_dfsservice_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_dfs_service_id_2438e833_fk_menus_dfsservice_id FOREIGN KEY (dfs_service_id) REFERENCES public.menus_dfsservice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdmenu menus_ussdmenu_input_screen_back_sc_74e6ebc5_fk_menus_uss; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_input_screen_back_sc_74e6ebc5_fk_menus_uss FOREIGN KEY (input_screen_back_screen_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdmenu menus_ussdmenu_menu_screen_back_scr_f2d39a43_fk_menus_uss; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_menu_screen_back_scr_f2d39a43_fk_menus_uss FOREIGN KEY (menu_screen_back_screen_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdmenu menus_ussdmenu_menu_type_id_d082a804_fk_menus_menutype_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_menu_type_id_d082a804_fk_menus_menutype_id FOREIGN KEY (menu_type_id) REFERENCES public.menus_menutype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdmenu menus_ussdmenu_next_screen_id_a244cc38_fk_menus_ussdmenu_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_next_screen_id_a244cc38_fk_menus_ussdmenu_id FOREIGN KEY (next_screen_id) REFERENCES public.menus_ussdmenu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: menus_ussdmenu menus_ussdmenu_shortcode_id_625c15cf_fk_menus_shortcode_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus_ussdmenu
    ADD CONSTRAINT menus_ussdmenu_shortcode_id_625c15cf_fk_menus_shortcode_id FOREIGN KEY (shortcode_id) REFERENCES public.menus_shortcode(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

